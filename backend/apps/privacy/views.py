"""
Privacy Views
API endpoints for DSAR management
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

from apps.events.models import Event

from .models import DSARRequest
from .serializers import (
    DSARRequestSerializer,
    DSARRequestCreateSerializer,
    DSARVerifySerializer,
    DSARApproveDeleteSerializer,
)


class DSARRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for DSAR request management.
    
    Endpoints:
    - POST /dsar/ - Create DSAR request (public)
    - GET /dsar/ - List DSAR requests (admin)
    - GET /dsar/{id}/ - Get DSAR details
    - POST /dsar/{id}/verify/ - Verify email
    - POST /dsar/{id}/approve-delete/ - Approve deletion (admin)
    """
    serializer_class = DSARRequestSerializer
    
    def get_queryset(self):
        """Return DSAR requests."""
        user = self.request.user
        
        # Admin sees all
        if user.is_staff:
            return DSARRequest.objects.all()
        
        # Users see their own
        if user.is_authenticated:
            return DSARRequest.objects.filter(user=user)
        
        return DSARRequest.objects.none()
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return DSARRequestCreateSerializer
        return DSARRequestSerializer
    
    def get_permissions(self):
        """Allow public DSAR creation."""
        if self.action == 'create':
            return [AllowAny()]
        if self.action == 'approve_delete':
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        """Create DSAR and send verification email."""
        # Check if user exists
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        email = serializer.validated_data['user_email']
        user = User.objects.filter(email=email).first()
        
        dsar = serializer.save(user=user)
        
        # Send verification email
        from .tasks import send_dsar_verification_email
        send_dsar_verification_email.delay(str(dsar.id))
        
        # Log event
        Event.log(
            event_type='dsar.created',
            email=dsar.user_email,
            request_type=dsar.request_type,
            dsar_id=str(dsar.id),
        )
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """
        Verify DSAR request via token.
        
        POST /dsar/{id}/verify/
        """
        dsar = self.get_object()
        
        if dsar.is_verified:
            return Response(
                {'error': 'Request already verified.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = DSARVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if str(dsar.verification_token) != str(serializer.validated_data['token']):
            return Response(
                {'error': 'Invalid verification token.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        dsar.verify()
        
        # If not a deletion, start processing automatically
        if not dsar.requires_approval:
            dsar.start_processing()
            from .tasks import process_dsar_export
            process_dsar_export.delay(str(dsar.id))
        
        return Response(DSARRequestSerializer(dsar).data)
    
    @action(detail=True, methods=['post'], url_path='approve-delete')
    def approve_delete(self, request, pk=None):
        """
        Approve deletion request (admin only).
        
        POST /dsar/{id}/approve-delete/
        """
        dsar = self.get_object()
        
        if dsar.request_type != 'delete':
            return Response(
                {'error': 'This is not a deletion request.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not dsar.is_verified:
            return Response(
                {'error': 'Request must be verified first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if dsar.is_approved:
            return Response(
                {'error': 'Deletion already approved.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = DSARApproveDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        dsar.approve_deletion(request.user)
        
        # Log event
        Event.log(
            event_type='dsar.deletion_approved',
            user_id=request.user.id,
            dsar_id=str(dsar.id),
            approved_by=request.user.email,
        )
        
        # Start processing
        dsar.start_processing()
        from .tasks import process_dsar_deletion
        process_dsar_deletion.delay(str(dsar.id))
        
        return Response(DSARRequestSerializer(dsar).data)
    
    @action(detail=False, methods=['get'], url_path='sla-dashboard')
    def sla_dashboard(self, request):
        """
        Get SLA dashboard stats (admin only).
        
        GET /dsar/sla-dashboard/
        """
        dsars = DSARRequest.objects.exclude(status__in=['completed', 'failed'])
        
        stats = {
            'within_sla': 0,
            'approaching_sla': 0,
            'breached_sla': 0,
            'pending_approval': 0,
        }
        
        for dsar in dsars:
            stats[dsar.sla_status] += 1
            if dsar.requires_approval and not dsar.is_approved:
                stats['pending_approval'] += 1
        
        return Response(stats)
