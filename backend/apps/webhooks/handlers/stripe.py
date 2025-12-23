"""
Stripe Webhook Handler
Handles Stripe webhook events for subscriptions and invoices
"""
import logging
from typing import Optional

from django.conf import settings
from django.utils import timezone

from apps.billing.models import Invoice
from apps.subscriptions.models import Subscription
from apps.events.models import Event
from apps.webhooks.models import WebhookEvent

logger = logging.getLogger(__name__)


class StripeWebhookHandler:
    """
    Handler for Stripe webhook events.
    
    Handles:
    - invoice.paid
    - invoice.payment_failed
    - customer.subscription.updated
    - customer.subscription.deleted
    """
    
    # Event type to handler mapping
    EVENT_HANDLERS = {
        'invoice.paid': 'handle_invoice_paid',
        'invoice.payment_failed': 'handle_invoice_payment_failed',
        'customer.subscription.updated': 'handle_subscription_updated',
        'customer.subscription.deleted': 'handle_subscription_deleted',
    }
    
    @classmethod
    def handle_event(cls, webhook_event: WebhookEvent) -> bool:
        """
        Route event to appropriate handler.
        
        Args:
            webhook_event: WebhookEvent record
            
        Returns:
            bool: True if handled successfully
        """
        event_type = webhook_event.event_type
        handler_name = cls.EVENT_HANDLERS.get(event_type)
        
        if not handler_name:
            logger.info(f"Unhandled Stripe event type: {event_type}")
            return True  # Not an error, just unhandled
        
        handler = getattr(cls, handler_name, None)
        if not handler:
            logger.error(f"Handler not found: {handler_name}")
            return False
        
        try:
            handler(webhook_event.payload)
            return True
        except Exception as e:
            logger.exception(f"Error handling {event_type}: {e}")
            return False
    
    @staticmethod
    def handle_invoice_paid(event_data: dict) -> None:
        """
        Handle invoice.paid event.
        
        Updates invoice status and triggers follow-up actions.
        """
        invoice_data = event_data.get('data', {}).get('object', {})
        stripe_invoice_id = invoice_data.get('id')
        
        if not stripe_invoice_id:
            logger.warning("invoice.paid: Missing invoice ID")
            return
        
        try:
            invoice = Invoice.objects.get(stripe_invoice_id=stripe_invoice_id)
        except Invoice.DoesNotExist:
            logger.info(f"invoice.paid: Invoice not found: {stripe_invoice_id}")
            return
        
        # Mark as paid
        payment_intent_id = invoice_data.get('payment_intent')
        invoice.mark_paid(payment_intent_id=payment_intent_id)
        
        # Log event
        Event.log(
            event_type='invoice.paid_webhook',
            organization_id=invoice.organization_id,
            invoice_id=str(invoice.id),
            stripe_invoice_id=stripe_invoice_id,
        )
        
        logger.info(f"invoice.paid: Marked invoice {invoice.id} as paid")
    
    @staticmethod
    def handle_invoice_payment_failed(event_data: dict) -> None:
        """
        Handle invoice.payment_failed event.
        
        Updates invoice and potentially subscription status.
        """
        invoice_data = event_data.get('data', {}).get('object', {})
        stripe_invoice_id = invoice_data.get('id')
        
        if not stripe_invoice_id:
            logger.warning("invoice.payment_failed: Missing invoice ID")
            return
        
        try:
            invoice = Invoice.objects.get(stripe_invoice_id=stripe_invoice_id)
        except Invoice.DoesNotExist:
            logger.info(f"invoice.payment_failed: Invoice not found: {stripe_invoice_id}")
            return
        
        # Update status
        invoice.status = 'open'  # Keep open for retry
        invoice.save(update_fields=['status', 'updated_at'])
        
        # Log event
        Event.log(
            event_type='invoice.payment_failed_webhook',
            organization_id=invoice.organization_id,
            invoice_id=str(invoice.id),
            stripe_invoice_id=stripe_invoice_id,
            failure_message=invoice_data.get('last_payment_error', {}).get('message'),
        )
        
        # TODO: Send payment failed notification email
        
        logger.warning(f"invoice.payment_failed: Invoice {invoice.id} payment failed")
    
    @staticmethod
    def handle_subscription_updated(event_data: dict) -> None:
        """
        Handle customer.subscription.updated event.
        
        Syncs subscription status from Stripe.
        """
        sub_data = event_data.get('data', {}).get('object', {})
        stripe_sub_id = sub_data.get('id')
        
        if not stripe_sub_id:
            logger.warning("subscription.updated: Missing subscription ID")
            return
        
        try:
            subscription = Subscription.objects.get(stripe_subscription_id=stripe_sub_id)
        except Subscription.DoesNotExist:
            logger.info(f"subscription.updated: Subscription not found: {stripe_sub_id}")
            return
        
        # Sync status
        old_status = subscription.status
        new_status = sub_data.get('status')
        
        if new_status and new_status != old_status:
            subscription.status = new_status
            subscription.save(update_fields=['status', 'updated_at'])
            
            # Log event
            Event.log(
                event_type='subscription.updated_webhook',
                organization_id=subscription.organization_id,
                subscription_id=str(subscription.id),
                old_status=old_status,
                new_status=new_status,
            )
            
            logger.info(f"subscription.updated: {subscription.id} status {old_status} → {new_status}")
    
    @staticmethod
    def handle_subscription_deleted(event_data: dict) -> None:
        """
        Handle customer.subscription.deleted event.
        
        Marks subscription as canceled.
        """
        sub_data = event_data.get('data', {}).get('object', {})
        stripe_sub_id = sub_data.get('id')
        
        if not stripe_sub_id:
            logger.warning("subscription.deleted: Missing subscription ID")
            return
        
        try:
            subscription = Subscription.objects.get(stripe_subscription_id=stripe_sub_id)
        except Subscription.DoesNotExist:
            logger.info(f"subscription.deleted: Subscription not found: {stripe_sub_id}")
            return
        
        # Mark as canceled
        subscription.status = 'canceled'
        subscription.canceled_at = timezone.now()
        subscription.save(update_fields=['status', 'canceled_at', 'updated_at'])
        
        # Log event
        Event.log(
            event_type='subscription.deleted_webhook',
            organization_id=subscription.organization_id,
            subscription_id=str(subscription.id),
        )
        
        logger.info(f"subscription.deleted: {subscription.id} canceled")
    
    @staticmethod
    def verify_signature(payload: bytes, sig_header: str, endpoint_secret: str) -> Optional[dict]:
        """
        Verify Stripe webhook signature.
        
        Args:
            payload: Raw request body
            sig_header: Stripe-Signature header
            endpoint_secret: Webhook endpoint secret
            
        Returns:
            dict: Parsed event if valid, None otherwise
        """
        try:
            import stripe
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
            return event
        except ValueError:
            logger.error("Invalid payload")
            return None
        except stripe.error.SignatureVerificationError:
            logger.error("Invalid signature")
            return None
