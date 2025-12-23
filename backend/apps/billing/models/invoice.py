"""
Invoice Model
GST-compliant invoicing with database-level calculation
"""
import uuid
from decimal import Decimal
from django.db import models
from django.db.models import F
from django.db.models.functions import Round
from django.utils import timezone


class Invoice(models.Model):
    """
    Invoice model with Singapore GST compliance.
    
    Features:
    - Django 6.0 GeneratedField for GST calculation
    - IRAS transaction code support
    - Stripe integration
    """
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('void', 'Void'),
        ('uncollectible', 'Uncollectible'),
    ]
    
    IRAS_CODE_CHOICES = [
        ('SR', 'Standard-Rated (9% GST)'),
        ('ZR', 'Zero-Rated'),
        ('OS', 'Out-of-Scope'),
        ('TX', 'Exempted'),
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
        related_name='invoices',
        help_text='Organization this invoice belongs to'
    )
    subscription = models.ForeignKey(
        'subscriptions.Subscription',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='invoices',
        help_text='Related subscription (if any)'
    )
    
    # Invoice number
    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        help_text='Human-readable invoice number'
    )
    
    # GST Calculation - CRITICAL
    subtotal_cents = models.BigIntegerField(
        help_text='Subtotal in cents before GST'
    )
    gst_rate = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        default=Decimal('0.0900'),
        help_text='GST rate (default 9% = 0.0900)'
    )
    
    # Generated fields for automatic calculation
    # Note: Django 6.0 GeneratedField with db_persist=True
    gst_amount_cents = models.GeneratedField(
        expression=Round(F('subtotal_cents') * F('gst_rate')),
        output_field=models.BigIntegerField(),
        db_persist=True,
    )
    
    total_amount_cents = models.GeneratedField(
        expression=F('subtotal_cents') + Round(F('subtotal_cents') * F('gst_rate')),
        output_field=models.BigIntegerField(),
        db_persist=True,
    )
    
    # IRAS compliance
    iras_transaction_code = models.CharField(
        max_length=2,
        choices=IRAS_CODE_CHOICES,
        default='SR',
        help_text='IRAS transaction code for GST reporting'
    )
    
    # Payment tracking
    amount_paid_cents = models.BigIntegerField(
        default=0,
        help_text='Amount paid in cents'
    )
    currency = models.CharField(
        max_length=3,
        default='SGD',
        help_text='Currency code'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        db_index=True
    )
    paid = models.BooleanField(
        default=False,
        help_text='Whether invoice is fully paid'
    )
    due_date = models.DateTimeField(
        help_text='Payment due date'
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When invoice was fully paid'
    )
    
    # Stripe integration
    stripe_invoice_id = models.CharField(
        max_length=255,
        unique=True,
        help_text='Stripe invoice ID'
    )
    stripe_payment_intent_id = models.CharField(
        max_length=255,
        blank=True,
        help_text='Stripe payment intent ID'
    )
    
    # Data
    pdf_url = models.URLField(
        blank=True,
        help_text='URL to invoice PDF'
    )
    line_items = models.JSONField(
        default=list,
        blank=True,
        help_text='Invoice line items'
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text='Additional metadata'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'invoices'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        ordering = ['-created_at']
        constraints = [
            # Amount paid cannot exceed total
            models.CheckConstraint(
                condition=models.Q(amount_paid_cents__lte=F('subtotal_cents') + Round(F('subtotal_cents') * F('gst_rate'))),
                name='amount_paid_not_exceed_total'
            ),
            # Paid invoices must have paid_at
            models.CheckConstraint(
                condition=~models.Q(paid=True) | models.Q(paid_at__isnull=False),
                name='paid_invoices_require_paid_at'
            ),
        ]
        indexes = [
            models.Index(fields=['organization', 'status']),
            models.Index(fields=['due_date']),
            models.Index(fields=['stripe_invoice_id']),
        ]
    
    def __str__(self):
        return f"Invoice {self.invoice_number or self.id} - {self.organization.name}"
    
    def save(self, *args, **kwargs):
        """Auto-generate invoice number if not provided."""
        if not self.invoice_number:
            # Format: INV-YYYYMM-XXXX
            from django.db.models import Max
            year_month = timezone.now().strftime('%Y%m')
            prefix = f"INV-{year_month}-"
            
            # Get the highest existing number for this month
            last_invoice = Invoice.objects.filter(
                invoice_number__startswith=prefix
            ).aggregate(Max('invoice_number'))['invoice_number__max']
            
            if last_invoice:
                try:
                    last_num = int(last_invoice.split('-')[-1])
                    new_num = last_num + 1
                except ValueError:
                    new_num = 1
            else:
                new_num = 1
            
            self.invoice_number = f"{prefix}{new_num:04d}"
        
        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self) -> bool:
        """Check if invoice is overdue."""
        if self.status == 'paid' or self.paid:
            return False
        return timezone.now() > self.due_date
    
    @property
    def days_overdue(self) -> int:
        """Get number of days overdue."""
        if not self.is_overdue:
            return 0
        delta = timezone.now() - self.due_date
        return delta.days
    
    @property
    def amount_due_cents(self) -> int:
        """Get remaining amount due."""
        if self.total_amount_cents is None:
            return 0
        return max(0, self.total_amount_cents - self.amount_paid_cents)
    
    @property
    def subtotal_dollars(self) -> Decimal:
        """Get subtotal in dollars."""
        return Decimal(self.subtotal_cents) / 100
    
    @property
    def gst_amount_dollars(self) -> Decimal:
        """Get GST amount in dollars."""
        if self.gst_amount_cents is None:
            return Decimal('0')
        return Decimal(self.gst_amount_cents) / 100
    
    @property
    def total_amount_dollars(self) -> Decimal:
        """Get total in dollars."""
        if self.total_amount_cents is None:
            return Decimal('0')
        return Decimal(self.total_amount_cents) / 100
    
    def mark_paid(self, payment_intent_id: str = None) -> None:
        """Mark invoice as paid."""
        self.status = 'paid'
        self.paid = True
        self.paid_at = timezone.now()
        self.amount_paid_cents = self.total_amount_cents or 0
        if payment_intent_id:
            self.stripe_payment_intent_id = payment_intent_id
        self.save()
    
    def void(self) -> None:
        """Void the invoice."""
        self.status = 'void'
        self.save(update_fields=['status', 'updated_at'])
