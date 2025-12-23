"""
Privacy Models
PDPA-compliant DSAR handling with 72-hour SLA
"""
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class DSARRequest(models.Model):
    """
    Data Subject Access Request for PDPA compliance.
    
    Features:
    - 72-hour SLA tracking
    - Manual approval for deletions
    - Verification flow
    - Export with expiration
    """
    
    REQUEST_TYPE_CHOICES = [
        ('export', 'Data Export'),
        ('delete', 'Data Deletion'),
        ('access', 'Data Access'),
        ('rectification', 'Data Rectification'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verifying', 'Verifying'),
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
    
    # Requester info
    user_email = models.EmailField(
        db_index=True,
        help_text='Email of the data subject'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='dsar_requests',
        help_text='Associated user account (if exists)'
    )
    
    # Request details
    request_type = models.CharField(
        max_length=20,
        choices=REQUEST_TYPE_CHOICES,
        db_index=True,
        help_text='Type of DSAR request'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True,
        help_text='Request status'
    )
    
    # Verification
    verification_token = models.UUIDField(
        default=uuid.uuid4,
        help_text='Token for email verification'
    )
    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When email was verified'
    )
    verification_method = models.CharField(
        max_length=50,
        blank=True,
        help_text='How verification was completed'
    )
    
    # Export
    export_url = models.URLField(
        blank=True,
        help_text='URL to download data export'
    )
    export_expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When export link expires (7 days)'
    )
    
    # Metadata
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text='Additional request metadata'
    )
    failure_reason = models.TextField(
        blank=True,
        help_text='Reason for failure (if any)'
    )
    
    # Timestamps
    requested_at = models.DateTimeField(auto_now_add=True)
    processing_started_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When processing began'
    )
    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When request was completed'
    )
    
    # Manual approval for deletions - CRITICAL
    deletion_approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='approved_dsar_deletions',
        help_text='Admin who approved deletion'
    )
    deletion_approved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When deletion was approved'
    )
    
    class Meta:
        db_table = 'dsar_requests'
        verbose_name = 'DSAR Request'
        verbose_name_plural = 'DSAR Requests'
        ordering = ['-requested_at']
        constraints = [
            # Completed DSAR must have processed_at
            models.CheckConstraint(
                condition=~models.Q(status='completed') | models.Q(processed_at__isnull=False),
                name='completed_dsar_requires_processed_at'
            ),
            # Deletion requests must be approved before completion
            models.CheckConstraint(
                condition=(
                    ~models.Q(request_type='delete', status='completed') |
                    models.Q(deletion_approved_by__isnull=False)
                ),
                name='deletion_requires_approval'
            ),
        ]
        indexes = [
            models.Index(fields=['user_email', 'status']),
            models.Index(fields=['requested_at']),
            models.Index(fields=['status', 'requested_at']),
        ]
    
    def __str__(self):
        return f"DSAR {self.id} - {self.request_type} ({self.status})"
    
    # SLA Constants (72 hours)
    SLA_HOURS = 72
    APPROACHING_THRESHOLD_HOURS = 48
    
    @property
    def sla_status(self) -> str:
        """
        Get SLA status based on 72-hour requirement.
        
        Returns:
            str: 'within_sla', 'approaching_sla', 'breached_sla', or 'completed'
        """
        if self.status == 'completed':
            return 'completed'
        
        hours_elapsed = self.hours_elapsed
        
        if hours_elapsed >= self.SLA_HOURS:
            return 'breached_sla'
        elif hours_elapsed >= self.APPROACHING_THRESHOLD_HOURS:
            return 'approaching_sla'
        else:
            return 'within_sla'
    
    @property
    def hours_elapsed(self) -> float:
        """Get hours since request was made."""
        delta = timezone.now() - self.requested_at
        return delta.total_seconds() / 3600
    
    @property
    def hours_remaining_in_sla(self) -> float:
        """Get hours remaining before SLA breach."""
        remaining = self.SLA_HOURS - self.hours_elapsed
        return max(0, remaining)
    
    @property
    def is_verified(self) -> bool:
        """Check if request has been verified."""
        return self.verified_at is not None
    
    @property
    def requires_approval(self) -> bool:
        """Check if this request requires manual approval."""
        return self.request_type == 'delete'
    
    @property
    def is_approved(self) -> bool:
        """Check if deletion has been approved."""
        if not self.requires_approval:
            return True  # Non-deletion requests don't need approval
        return self.deletion_approved_by is not None
    
    def verify(self, method: str = 'email') -> None:
        """Mark request as verified."""
        self.status = 'verifying'
        self.verified_at = timezone.now()
        self.verification_method = method
        self.save(update_fields=['status', 'verified_at', 'verification_method', 'requested_at'])
    
    def start_processing(self) -> None:
        """Mark request as processing."""
        self.status = 'processing'
        self.processing_started_at = timezone.now()
        self.save(update_fields=['status', 'processing_started_at'])
    
    def complete(self, export_url: str = None) -> None:
        """Mark request as completed."""
        from datetime import timedelta
        
        self.status = 'completed'
        self.processed_at = timezone.now()
        
        if export_url:
            self.export_url = export_url
            self.export_expires_at = timezone.now() + timedelta(days=7)
        
        self.save()
    
    def fail(self, reason: str) -> None:
        """Mark request as failed."""
        self.status = 'failed'
        self.failure_reason = reason
        self.processed_at = timezone.now()
        self.save(update_fields=['status', 'failure_reason', 'processed_at'])
    
    def approve_deletion(self, approved_by) -> None:
        """Approve deletion request."""
        self.deletion_approved_by = approved_by
        self.deletion_approved_at = timezone.now()
        self.save(update_fields=['deletion_approved_by', 'deletion_approved_at'])
