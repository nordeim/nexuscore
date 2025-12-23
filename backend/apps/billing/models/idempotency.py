"""
Idempotency Record Model
Prevents duplicate operations for payment-critical endpoints (PRD-d-3)
"""
import uuid
from django.db import models
from django.utils import timezone


class IdempotencyRecord(models.Model):
    """
    Track idempotency keys to prevent duplicate operations.
    
    Critical for:
    - Payment processing
    - Subscription creation
    - Invoice generation
    
    Per PRD-d-3, this model stores the request/response pair to enable
    safe retries of failed operations.
    """
    
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    # Primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Idempotency key (from Idempotency-Key header)
    key = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text='Unique idempotency key from request header'
    )
    
    # Request metadata
    request_path = models.CharField(
        max_length=255,
        help_text='API endpoint path'
    )
    request_method = models.CharField(
        max_length=10,
        help_text='HTTP method (POST, PUT, etc.)'
    )
    request_hash = models.CharField(
        max_length=64,
        help_text='SHA256 hash of request body for collision detection'
    )
    
    # Processing status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='processing'
    )
    
    # Cached response (for completed requests)
    response_status_code = models.IntegerField(
        null=True,
        blank=True,
        help_text='HTTP status code of the response'
    )
    response_body = models.JSONField(
        null=True,
        blank=True,
        help_text='Cached response body for replay'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(
        help_text='When this idempotency record expires (typically 24h)'
    )
    
    class Meta:
        db_table = 'idempotency_records'
        verbose_name = 'Idempotency Record'
        verbose_name_plural = 'Idempotency Records'
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['request_path', 'request_method']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Idempotency: {self.key[:20]}... ({self.status})"
    
    def is_expired(self) -> bool:
        """Check if this idempotency record has expired."""
        return timezone.now() > self.expires_at
    
    def can_be_replayed(self) -> bool:
        """Check if this record can be used to replay a response."""
        return (
            self.status == 'completed' and
            self.response_status_code is not None and
            not self.is_expired()
        )
    
    @classmethod
    def cleanup_expired(cls):
        """Delete expired idempotency records."""
        return cls.objects.filter(expires_at__lt=timezone.now()).delete()
