"""
Billing Admin Configuration
Django admin for Invoice and IdempotencyRecord models
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import IdempotencyRecord, Invoice


@admin.register(IdempotencyRecord)
class IdempotencyRecordAdmin(admin.ModelAdmin):
    """Admin for IdempotencyRecord model."""
    
    list_display = ['key', 'request_method', 'request_path', 'status', 'created_at']
    list_filter = ['status', 'request_method', 'created_at']
    search_fields = ['key', 'request_path']
    readonly_fields = ['created_at']
    ordering = ['-created_at']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """Admin for Invoice model."""
    
    list_display = [
        'invoice_number',
        'organization',
        'subtotal_display',
        'gst_display',
        'total_display',
        'status_badge',
        'due_date',
        'created_at',
    ]
    list_filter = [
        'status',
        'paid',
        'iras_transaction_code',
        'currency',
        'created_at',
    ]
    search_fields = [
        'invoice_number',
        'organization__name',
        'organization__uen',
        'stripe_invoice_id',
    ]
    ordering = ['-created_at']
    readonly_fields = [
        'invoice_number',
        'gst_amount_cents',
        'total_amount_cents',
        'created_at',
        'updated_at',
    ]
    autocomplete_fields = ['organization', 'subscription']
    
    fieldsets = (
        (None, {
            'fields': ('invoice_number', 'organization', 'subscription')
        }),
        ('Amounts (GST Auto-Calculated)', {
            'fields': (
                'subtotal_cents',
                'gst_rate',
                'gst_amount_cents',
                'total_amount_cents',
                'currency',
            ),
            'description': 'GST and total are calculated automatically by the database.'
        }),
        ('IRAS Compliance', {
            'fields': ('iras_transaction_code',),
            'description': 'SR=Standard-Rated (9%), ZR=Zero-Rated, OS=Out-of-Scope, TX=Exempted'
        }),
        ('Payment', {
            'fields': ('status', 'amount_paid_cents', 'paid', 'due_date', 'paid_at')
        }),
        ('Stripe', {
            'fields': ('stripe_invoice_id', 'stripe_payment_intent_id'),
            'classes': ('collapse',)
        }),
        ('Data', {
            'fields': ('pdf_url', 'line_items', 'metadata'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def subtotal_display(self, obj):
        """Display subtotal in dollars."""
        return f"${obj.subtotal_cents / 100:.2f}"
    subtotal_display.short_description = 'Subtotal'
    
    def gst_display(self, obj):
        """Display GST amount in dollars."""
        if obj.gst_amount_cents:
            return f"${obj.gst_amount_cents / 100:.2f}"
        return '-'
    gst_display.short_description = 'GST (9%)'
    
    def total_display(self, obj):
        """Display total in dollars."""
        if obj.total_amount_cents:
            return f"${obj.total_amount_cents / 100:.2f}"
        return '-'
    total_display.short_description = 'Total'
    
    def status_badge(self, obj):
        """Display status as colored badge."""
        colors = {
            'draft': 'gray',
            'open': 'blue',
            'paid': 'green',
            'void': 'red',
            'uncollectible': 'orange',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
