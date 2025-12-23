"""
Webhook Celery Tasks
Background tasks for webhook processing
"""
import logging
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(queue='high', bind=True, max_retries=3)
def process_stripe_webhook(self, webhook_event_id: str) -> dict:
    """
    Process a Stripe webhook event.
    
    Args:
        webhook_event_id: UUID of the WebhookEvent
        
    Returns:
        dict: Processing result
    """
    from .models import WebhookEvent
    from .handlers.stripe import StripeWebhookHandler
    
    try:
        webhook_event = WebhookEvent.objects.get(id=webhook_event_id)
    except WebhookEvent.DoesNotExist:
        logger.error(f"WebhookEvent not found: {webhook_event_id}")
        return {'error': 'WebhookEvent not found'}
    
    if webhook_event.processed:
        logger.info(f"WebhookEvent already processed: {webhook_event_id}")
        return {'status': 'already_processed'}
    
    # Mark processing time
    webhook_event.last_retry_at = timezone.now()
    webhook_event.save(update_fields=['last_retry_at'])
    
    try:
        # Handle the event
        success = StripeWebhookHandler.handle_event(webhook_event)
        
        if success:
            webhook_event.mark_processed()
            logger.info(f"WebhookEvent processed: {webhook_event_id}")
            return {'status': 'processed'}
        else:
            raise Exception("Handler returned False")
            
    except Exception as e:
        error_msg = str(e)
        logger.exception(f"Error processing webhook {webhook_event_id}: {error_msg}")
        
        webhook_event.mark_failed(error_msg)
        
        # Retry with exponential backoff
        if self.request.retries < self.max_retries:
            countdown = 60 * (2 ** self.request.retries)  # 60s, 120s, 240s
            raise self.retry(exc=e, countdown=countdown)
        
        return {'error': error_msg}


@shared_task(queue='high')
def process_stripe_subscription(
    subscription_id: str,
    payment_method_id: str,
    idempotency_key: str
) -> dict:
    """
    Create or update subscription in Stripe.
    
    Args:
        subscription_id: UUID of local Subscription
        payment_method_id: Stripe payment method ID
        idempotency_key: Idempotency key for Stripe
        
    Returns:
        dict: Stripe subscription data
    """
    from apps.subscriptions.models import Subscription
    
    try:
        subscription = Subscription.objects.select_related('plan', 'organization').get(
            id=subscription_id
        )
    except Subscription.DoesNotExist:
        return {'error': 'Subscription not found'}
    
    # TODO: Implement actual Stripe subscription creation
    # import stripe
    # stripe.api_key = settings.STRIPE_SECRET_KEY
    # 
    # stripe_sub = stripe.Subscription.create(
    #     customer=subscription.stripe_customer_id,
    #     items=[{'price': subscription.plan.stripe_price_id}],
    #     payment_behavior='default_incomplete',
    #     expand=['latest_invoice.payment_intent'],
    #     idempotency_key=idempotency_key,
    # )
    
    return {'status': 'created', 'subscription_id': subscription_id}


@shared_task
def cleanup_old_webhook_events() -> dict:
    """
    Clean up old webhook events.
    Run via Celery beat.
    
    Returns:
        dict: Cleanup results
    """
    from datetime import timedelta
    from .models import WebhookEvent
    
    # Delete processed events older than 30 days
    threshold = timezone.now() - timedelta(days=30)
    
    deleted, _ = WebhookEvent.objects.filter(
        status='processed',
        created_at__lt=threshold
    ).delete()
    
    return {'deleted': deleted}
