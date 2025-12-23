"""
Lead Views
API endpoints for lead management
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.events.models import Event

from .models import Lead
from .serializers import (
    LeadSerializer,
    LeadCreateSerializer,
    LeadUpdateSerializer,
)


class LeadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for lead management.
    
    Endpoints:
    - POST /leads/ - Create lead (public)
    - GET /leads/ - List leads (authenticated)
    - GET /leads/{id}/ - Get lead details
    - PATCH /leads/{id}/ - Update lead
    - POST /leads/{id}/convert/ - Convert lead to user
    """
    serializer_class = LeadSerializer
    
    def get_queryset(self):
        """Return leads, optionally filtered."""
        qs = Lead.objects.all()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        
        # Filter by source
        source_filter = self.request.query_params.get('source')
        if source_filter:
            qs = qs.filter(source=source_filter)
        
        # Filter by assigned_to
        assigned_to = self.request.query_params.get('assigned_to')
        if assigned_to:
            qs = qs.filter(assigned_to_id=assigned_to)
        
        return qs.select_related('assigned_to', 'converted_to_user')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return LeadCreateSerializer
        if self.action in ['update', 'partial_update']:
            return LeadUpdateSerializer
        return LeadSerializer
    
    def get_permissions(self):
        """Allow public lead creation."""
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        """Create lead and log event."""
        lead = serializer.save()
        
        # Log event
        Event.log(
            event_type='lead.created',
            email=lead.email,
            source=lead.source,
            lead_id=str(lead.id),
        )
    
    @action(detail=True, methods=['post'])
    def convert(self, request, pk=None):
        """
        Convert lead to user.
        
        POST /leads/{id}/convert/
        
        Body:
        - user_id: UUID of user to associate
        """
        lead = self.get_object()
        
        if lead.is_converted:
            return Response(
                {'error': 'Lead is already converted.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        lead.convert_to_user(user)
        
        # Log event
        Event.log(
            event_type='lead.converted',
            user_id=user.id,
            lead_id=str(lead.id),
        )
        
        return Response(LeadSerializer(lead).data)
    
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        """
        Assign lead to a user.
        
        POST /leads/{id}/assign/
        
        Body:
        - user_id: UUID of user to assign
        """
        lead = self.get_object()
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        lead.assigned_to = user
        lead.save(update_fields=['assigned_to', 'updated_at'])
        
        return Response(LeadSerializer(lead).data)
