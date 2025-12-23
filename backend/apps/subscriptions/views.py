"""
Subscription Views
API endpoints for plan and subscription management
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone

from apps.billing.models import IdempotencyRecord
from apps.core.exceptions import IdempotencyConflict
from apps.events.models import Event

from .models import Plan, Subscription
from .serializers import (
    PlanSerializer,
    SubscriptionSerializer,
    SubscriptionCreateSerializer,
    CancelSubscriptionSerializer,
)
from .services import SubscriptionService


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for reading plans (public).
    
    Endpoints:
    - GET /plans/ - List visible plans
    - GET /plans/{id}/ - Get plan details
    """
    serializer_class = PlanSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        """Return visible, active plans."""
        return Plan.objects.filter(is_active=True, is_visible=True)


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for subscription management.
    
    Endpoints:
    - GET /subscriptions/ - List user's subscriptions
    - POST /subscriptions/ - Create subscription (requires Idempotency-Key)
    - GET /subscriptions/{id}/ - Get subscription details
    - POST /subscriptions/{id}/cancel/ - Cancel subscription
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return subscriptions for user's organizations."""
        return Subscription.objects.filter(
            organization__memberships__user=self.request.user
        ).select_related('plan', 'organization').distinct()
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return SubscriptionCreateSerializer
        return SubscriptionSerializer
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create a new subscription.
        
        CRITICAL: Requires Idempotency-Key header.
        """
        # Check idempotency key
        idempotency_key = request.headers.get('Idempotency-Key')
        if not idempotency_key:
            return Response(
                {'error': 'Idempotency-Key header is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check for existing idempotency record
        existing = IdempotencyRecord.objects.filter(key=idempotency_key).first()
        if existing:
            if existing.can_be_replayed():
                return Response(
                    existing.response_body,
                    status=existing.response_status_code
                )
            raise IdempotencyConflict(
                f"Request with idempotency key '{idempotency_key}' is still processing"
            )
        
        # Create idempotency record
        idempotency_record = IdempotencyRecord.objects.create(
            key=idempotency_key,
            request_path=request.path,
            request_method=request.method,
            status='processing'
        )
        
        try:
            # Validate request
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Create subscription via service
            subscription = SubscriptionService.create_subscription(
                organization_id=serializer.validated_data['organization_id'],
                plan_id=serializer.validated_data['plan_id'],
                user=request.user
            )
            
            # Log event
            Event.log(
                event_type='subscription.created',
                user_id=request.user.id,
                organization_id=subscription.organization_id,
                plan_id=str(subscription.plan_id),
                subscription_id=str(subscription.id),
            )
            
            # Prepare response
            response_data = SubscriptionSerializer(subscription).data
            
            # Update idempotency record
            idempotency_record.status = 'completed'
            idempotency_record.response_status_code = 201
            idempotency_record.response_body = response_data
            idempotency_record.save()
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            # Mark idempotency record as failed
            idempotency_record.status = 'failed'
            idempotency_record.save()
            raise
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel a subscription.
        
        POST /subscriptions/{id}/cancel/
        
        Body:
        - at_period_end: bool (default True)
        """
        subscription = self.get_object()
        
        # Check permissions
        if not subscription.organization.memberships.filter(
            user=request.user,
            role__in=['owner', 'admin']
        ).exists():
            return Response(
                {'error': 'You must be an admin to cancel subscriptions.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = CancelSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Cancel subscription
        subscription.cancel(at_period_end=serializer.validated_data['at_period_end'])
        
        # Log event
        Event.log(
            event_type='subscription.canceled',
            user_id=request.user.id,
            organization_id=subscription.organization_id,
            subscription_id=str(subscription.id),
            at_period_end=serializer.validated_data['at_period_end'],
        )
        
        return Response(SubscriptionSerializer(subscription).data)
