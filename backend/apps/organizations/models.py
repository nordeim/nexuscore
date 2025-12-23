"""
Organization Models
Singapore UEN/GST compliance with multi-tenant membership
"""
import uuid
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from apps.core.validators import UENValidator, GSTRegNoValidator

# Use string reference for User model to avoid circular imports
USER_MODEL = 'users.User'


class Organization(models.Model):
    """
    Organization model with Singapore compliance.
    
    Features:
    - UEN (Unique Entity Number) validation per ACRA
    - GST registration number validation per IRAS
    - Multi-tenant membership system
    - Trial period tracking
    """
    
    # Primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Basic info
    name = models.CharField(
        max_length=255,
        help_text='Organization name'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text='URL-friendly identifier'
    )
    
    # Singapore Compliance - CRITICAL
    uen = models.CharField(
        max_length=15,
        unique=True,
        validators=[UENValidator],
        help_text='Singapore Unique Entity Number (ACRA)'
    )
    is_gst_registered = models.BooleanField(
        default=False,
        help_text='Whether organization is GST registered'
    )
    gst_reg_no = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[GSTRegNoValidator],
        help_text='GST Registration Number (IRAS format: M12345678A)'
    )
    
    # Billing
    stripe_customer_id = models.CharField(
        max_length=255,
        blank=True,
        help_text='Stripe customer ID'
    )
    billing_email = models.EmailField(
        help_text='Email for billing notifications'
    )
    billing_phone = models.CharField(
        max_length=20,
        blank=True,
        help_text='Phone for billing contact'
    )
    billing_address = models.JSONField(
        default=dict,
        blank=True,
        help_text='Billing address as JSON'
    )
    
    # Settings (renamed from 'settings' to avoid shadowing)
    org_timezone = models.CharField(
        max_length=50,
        default='Asia/Singapore',
        help_text='Organization timezone',
        db_column='timezone'
    )
    locale = models.CharField(
        max_length=10,
        default='en-SG',
        help_text='Locale for formatting'
    )
    org_settings = models.JSONField(
        default=dict,
        blank=True,
        help_text='Organization settings',
        db_column='settings'
    )
    
    # Relationships
    owner = models.ForeignKey(
        USER_MODEL,
        on_delete=models.PROTECT,
        related_name='owned_organizations',
        help_text='Organization owner'
    )
    members = models.ManyToManyField(
        USER_MODEL,
        through='OrganizationMembership',
        through_fields=('organization', 'user'),
        related_name='organizations',
        help_text='Organization members'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trial_ends_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When trial period ends'
    )
    
    class Meta:
        db_table = 'organizations'
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        ordering = ['name']
        constraints = [
            # If GST registered, must have GST reg number
            models.CheckConstraint(
                condition=models.Q(is_gst_registered=False) | models.Q(gst_reg_no__isnull=False),
                name='valid_gst_registration'
            ),
        ]
        indexes = [
            models.Index(fields=['uen']),
            models.Index(fields=['slug']),
            models.Index(fields=['owner']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.uen})"
    
    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure uniqueness
            base_slug = self.slug
            counter = 1
            while Organization.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    @property
    def is_in_trial(self) -> bool:
        """Check if organization is in trial period."""
        if self.trial_ends_at is None:
            return False
        return timezone.now() < self.trial_ends_at
    
    @property
    def days_left_in_trial(self) -> int:
        """Get days remaining in trial."""
        if not self.is_in_trial:
            return 0
        delta = self.trial_ends_at - timezone.now()
        return max(0, delta.days)


class OrganizationMembership(models.Model):
    """
    Organization membership with role-based access.
    
    Roles:
    - owner: Full control
    - admin: Manage members, settings
    - member: Standard access
    - viewer: Read-only access
    """
    
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Administrator'),
        ('member', 'Member'),
        ('viewer', 'Viewer'),
    ]
    
    # Primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Relationships
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    
    # Role and permissions
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member'
    )
    permissions = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        help_text='Additional permissions beyond role'
    )
    
    # Invitation tracking
    invited_by = models.ForeignKey(
        USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='sent_invitations'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'organization_memberships'
        verbose_name = 'Organization Membership'
        verbose_name_plural = 'Organization Memberships'
        unique_together = [('organization', 'user')]
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.organization.name} ({self.role})"
    
    @property
    def is_owner(self) -> bool:
        """Check if user is organization owner."""
        return self.role == 'owner'
    
    @property
    def is_admin(self) -> bool:
        """Check if user is admin or owner."""
        return self.role in ('owner', 'admin')
    
    def has_permission(self, permission: str) -> bool:
        """Check if membership has a specific permission."""
        # Owners have all permissions
        if self.role == 'owner':
            return True
        return permission in self.permissions
