"""
Subscription Models
Plan and Subscription management with Stripe integration
"""
import uuid
from decimal import Decimal
from django.db import models
from django.utils import timezone


class Plan(models.Model):
    """
    Subscription plan with pricing and features.
    
    Features:
    - SGD currency default
    - Stripe integration
    - Feature flags and limits
    """
    
    BILLING_PERIOD_CHOICES = [
        ('month', 'Monthly'),
        ('year', 'Yearly'),
    ]
    
    # Primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Plan details
    name = models.CharField(
        max_length=100,
        help_text='Plan display name'
    )
    description = models.TextField(
        blank=True,
        help_text='Plan description'
    )
    sku = models.CharField(
        max_length=50,
        unique=True,
        help_text='Unique plan identifier'
    )
    
    # Pricing
    billing_period = models.CharField(
        max_length=10,
        choices=BILLING_PERIOD_CHOICES,
        default='month',
        help_text='Billing cycle'
    )
    amount_cents = models.PositiveIntegerField(
        help_text='Price in cents (e.g., 2999 = $29.99)'
    )
    currency = models.CharField(
        max_length=3,
        default='SGD',
        help_text='Currency code'
    )
    
    # Features and limits
    features = models.JSONField(
        default=dict,
        blank=True,
        help_text='Feature flags (e.g., {"api_access": true})'
    )
    limits = models.JSONField(
        default=dict,
        blank=True,
        help_text='Usage limits (e.g., {"users": 10, "storage_gb": 50})'
    )
    
    # Display
    is_active = models.BooleanField(
        default=True,
        help_text='Whether plan can be purchased'
    )
    is_visible = models.BooleanField(
        default=True,
        help_text='Whether plan is shown on pricing page'
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text='Order on pricing page'
    )
    
    # Stripe integration
    stripe_product_id = models.CharField(
        max_length=255,
        blank=True,
        help_text='Stripe product ID'
    )
    stripe_price_id = models.CharField(
        max_length=255,
        blank=True,
        help_text='Stripe price ID'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'plans'
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'
        ordering = ['display_order', 'created_at']
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    @property
    def amount_dollars(self) -> Decimal:
        """Get amount in dollars."""
        return Decimal(self.amount_cents) / 100
    
    @property
    def formatted_price(self) -> str:
        """Get formatted price string."""
        return f"${self.amount_dollars:.2f} {self.currency}/{self.billing_period}"


class Subscription(models.Model):
    """
    Organization subscription to a plan.
    
    Features:
    - Status tracking (trialing, active, etc.)
    - Stripe integration
    - Period management
    """
    
    STATUS_CHOICES = [
        ('trialing', 'Trialing'),
        ('active', 'Active'),
        ('past_due', 'Past Due'),
        ('canceled', 'Canceled'),
        ('unpaid', 'Unpaid'),
    ]
    
    # Primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Relationships
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.PROTECT,
        related_name='subscriptions',
        help_text='Organization this subscription belongs to'
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name='subscriptions',
        help_text='Subscribed plan'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='trialing',
        db_index=True
    )
    cancel_at_period_end = models.BooleanField(
        default=False,
        help_text='Whether to cancel at period end'
    )
    
    # Period
    current_period_start = models.DateTimeField(
        help_text='Start of current billing period'
    )
    current_period_end = models.DateTimeField(
        help_text='End of current billing period'
    )
    
    # Trial
    trial_start = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Trial start date'
    )
    trial_end = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Trial end date'
    )
    
    # Stripe integration
    stripe_subscription_id = models.CharField(
        max_length=255,
        unique=True,
        help_text='Stripe subscription ID'
    )
    stripe_customer_id = models.CharField(
        max_length=255,
        help_text='Stripe customer ID'
    )
    stripe_latest_invoice_id = models.CharField(
        max_length=255,
        blank=True,
        help_text='Latest Stripe invoice ID'
    )
    
    # Metadata
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text='Additional metadata'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    canceled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When subscription was canceled'
    )
    
    class Meta:
        db_table = 'subscriptions'
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        ordering = ['-created_at']
        constraints = [
            # Period end must be after start
            models.CheckConstraint(
                condition=models.Q(current_period_end__gt=models.F('current_period_start')),
                name='period_end_after_start'
            ),
            # If trialing status, trial_end must be set
            models.CheckConstraint(
                condition=~models.Q(status='trialing') | models.Q(trial_end__isnull=False),
                name='trial_status_requires_trial_end'
            ),
        ]
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['status', 'organization']),
            models.Index(fields=['stripe_subscription_id']),
        ]
    
    def __str__(self):
        return f"{self.organization.name} - {self.plan.name} ({self.status})"
    
    @property
    def is_active(self) -> bool:
        """Check if subscription is active."""
        return self.status in ('active', 'trialing')
    
    @property
    def is_in_trial(self) -> bool:
        """Check if subscription is in trial."""
        if self.status != 'trialing':
            return False
        if self.trial_end is None:
            return False
        return timezone.now() < self.trial_end
    
    @property
    def days_until_renewal(self) -> int:
        """Get days until next billing."""
        if self.current_period_end is None:
            return 0
        delta = self.current_period_end - timezone.now()
        return max(0, delta.days)
    
    def cancel(self, at_period_end: bool = True) -> None:
        """Cancel the subscription."""
        self.cancel_at_period_end = at_period_end
        if not at_period_end:
            self.status = 'canceled'
            self.canceled_at = timezone.now()
        self.save(update_fields=['cancel_at_period_end', 'status', 'canceled_at', 'updated_at'])
