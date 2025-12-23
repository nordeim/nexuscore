"""
Webhook Views
API endpoints for receiving webhooks
"""
import logging
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WebhookEvent
from .handlers.stripe import StripeWebhookHandler

logger = logging.getLogger(__name__)


class StripeWebhookView(APIView):
    """
    Stripe webhook endpoint.
    
    POST /webhooks/stripe/
    
    Flow:
    1. Verify signature
    2. Check for duplicate event
    3. Create WebhookEvent record
    4. Enqueue processing task
    5. Return 200 immediately
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Handle incoming Stripe webhook."""
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        
        # Get endpoint secret from settings
        endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', None)
        
        if not endpoint_secret:
            logger.error("STRIPE_WEBHOOK_SECRET not configured")
            # Still return 200 to avoid Stripe retries
            return Response({'status': 'configuration_error'}, status=status.HTTP_200_OK)
        
        # Verify signature
        event = StripeWebhookHandler.verify_signature(payload, sig_header, endpoint_secret)
        if not event:
            # Return 400 for invalid signature
            return Response(
                {'error': 'Invalid signature'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        event_id = event.get('id')
        event_type = event.get('type')
        
        # Check for duplicate (idempotency)
        existing = WebhookEvent.objects.filter(
            event_id=event_id,
            service='stripe'
        ).first()
        
        if existing:
            logger.info(f"Duplicate Stripe event: {event_id}")
            # Return 200 for duplicates (don't trigger retries)
            return Response({'status': 'duplicate'}, status=status.HTTP_200_OK)
        
        # Create WebhookEvent record
        webhook_event = WebhookEvent.objects.create(
            service='stripe',
            event_id=event_id,
            event_type=event_type,
            payload=event
        )
        
        logger.info(f"Created WebhookEvent: {webhook_event.id} ({event_type})")
        
        # Enqueue processing task
        from .tasks import process_stripe_webhook
        process_stripe_webhook.delay(str(webhook_event.id))
        
        # Return 200 immediately (async processing)
        return Response({'status': 'accepted'}, status=status.HTTP_200_OK)
