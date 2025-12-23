"""
WebhookEvent Model
Track external webhook events from Stripe, SendGrid, etc. (PRD-d-3)
"""
import uuid
from django.db import models
from django.utils import timezone


class WebhookEvent(models.Model):
    """
    Track and process webhook events from external services.
    
    Provides:
    - Deduplication (unique event_id per service)
    - Retry tracking
    - Error logging
    - Processing status
    
    Used for:
    - Stripe payment events
    - SendGrid email events
    - Other third-party integrations
    """
    
    # Primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Source service
    service = models.CharField(
        max_length=50,
        db_index=True,
        help_text='Service name (e.g., stripe, sendgrid)'
    )
    
    # External event ID (unique per service)
    event_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text='External event ID from the service'
    )
    
    # Event type
    event_type = models.CharField(
        max_length=100,
        db_index=True,
        help_text='Event type (e.g., invoice.paid, customer.subscription.created)'
    )
    
    # Raw payload
    payload = models.JSONField(
        help_text='Raw webhook payload from the service'
    )
    
    # Processing status
    processed = models.BooleanField(
        default=False,
        db_index=True,
        help_text='Whether the event has been successfully processed'
    )
    processing_error = models.TextField(
        blank=True,
        help_text='Error message if processing failed'
    )
    
    # Retry tracking
    retry_count = models.PositiveIntegerField(
        default=0,
        help_text='Number of processing retry attempts'
    )
    last_retry_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp of last retry attempt'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When the event was successfully processed'
    )
    
    class Meta:
        db_table = 'webhook_events'
        verbose_name = 'Webhook Event'
        verbose_name_plural = 'Webhook Events'
        indexes = [
            models.Index(fields=['service', 'event_type']),
            models.Index(fields=['processed', 'created_at']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        status = '✓' if self.processed else '✗'
        return f"Webhook [{status}]: {self.service}/{self.event_type}"
    
    def mark_processed(self):
        """Mark the event as successfully processed."""
        self.processed = True
        self.processed_at = timezone.now()
        self.save(update_fields=['processed', 'processed_at'])
    
    def mark_failed(self, error: str):
        """Mark the event as failed with error message."""
        self.processing_error = error
        self.retry_count += 1
        self.last_retry_at = timezone.now()
        self.save(update_fields=['processing_error', 'retry_count', 'last_retry_at'])
    
    @property
    def can_retry(self) -> bool:
        """Check if the event can be retried (max 5 retries)."""
        return not self.processed and self.retry_count < 5
    
    @classmethod
    def get_pending(cls, service: str = None, limit: int = 100):
        """Get pending (unprocessed) webhook events."""
        qs = cls.objects.filter(processed=False, retry_count__lt=5)
        if service:
            qs = qs.filter(service=service)
        return qs.order_by('created_at')[:limit]
