"""
Lead Models
Marketing lead capture with UTM tracking
"""
import uuid
from django.conf import settings
from django.db import models


class Lead(models.Model):
    """
    Marketing lead for capture and conversion tracking.
    
    Features:
    - Multiple lead sources
    - Status progression tracking
    - Full UTM parameter support
    - Conversion to user tracking
    """
    
    SOURCE_CHOICES = [
        ('website', 'Website'),
        ('demo_request', 'Demo Request'),
        ('contact', 'Contact Form'),
        ('event', 'Event'),
        ('referral', 'Referral'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('disqualified', 'Disqualified'),
    ]
    
    # Primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Contact info
    name = models.CharField(
        max_length=255,
        help_text='Lead name'
    )
    email = models.EmailField(
        db_index=True,
        help_text='Lead email address'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text='Phone number'
    )
    company = models.CharField(
        max_length=255,
        help_text='Company name'
    )
    job_title = models.CharField(
        max_length=100,
        blank=True,
        help_text='Job title'
    )
    
    # Lead management
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default='website',
        db_index=True,
        help_text='Lead source'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        db_index=True,
        help_text='Lead status'
    )
    notes = models.TextField(
        blank=True,
        help_text='Internal notes'
    )
    
    # UTM tracking
    utm_source = models.CharField(
        max_length=100,
        blank=True,
        help_text='UTM source (e.g., google, linkedin)'
    )
    utm_medium = models.CharField(
        max_length=100,
        blank=True,
        help_text='UTM medium (e.g., cpc, email)'
    )
    utm_campaign = models.CharField(
        max_length=100,
        blank=True,
        help_text='UTM campaign name'
    )
    utm_term = models.CharField(
        max_length=100,
        blank=True,
        help_text='UTM term (paid search keywords)'
    )
    utm_content = models.CharField(
        max_length=100,
        blank=True,
        help_text='UTM content (ad variant)'
    )
    
    # Form data
    form_data = models.JSONField(
        default=dict,
        blank=True,
        help_text='Raw form submission data'
    )
    
    # Assignment
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_leads',
        help_text='Assigned sales rep'
    )
    next_follow_up = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Next follow-up date'
    )
    
    # Conversion tracking
    converted_to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='converted_from_lead',
        help_text='User created from this lead'
    )
    converted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When lead was converted to user'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leads'
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['source', 'status']),
            models.Index(fields=['assigned_to', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    @property
    def is_converted(self) -> bool:
        """Check if lead has been converted."""
        return self.status == 'converted' and self.converted_to_user is not None
    
    def convert_to_user(self, user) -> None:
        """Mark lead as converted to a user."""
        from django.utils import timezone
        self.status = 'converted'
        self.converted_to_user = user
        self.converted_at = timezone.now()
        self.save(update_fields=['status', 'converted_to_user', 'converted_at', 'updated_at'])
