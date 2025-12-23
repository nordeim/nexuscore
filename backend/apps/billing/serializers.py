"""
Billing Serializers
DRF serializers for Invoice model
"""
from rest_framework import serializers
from decimal import Decimal

from .models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for reading invoice data."""
    
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    subtotal_dollars = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    gst_amount_dollars = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_amount_dollars = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    amount_due_cents = serializers.IntegerField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    days_overdue = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Invoice
        fields = [
            'id',
            'invoice_number',
            'organization',
            'organization_name',
            'subscription',
            'subtotal_cents',
            'subtotal_dollars',
            'gst_rate',
            'gst_amount_cents',
            'gst_amount_dollars',
            'total_amount_cents',
            'total_amount_dollars',
            'iras_transaction_code',
            'amount_paid_cents',
            'amount_due_cents',
            'currency',
            'status',
            'paid',
            'due_date',
            'paid_at',
            'pdf_url',
            'line_items',
            'is_overdue',
            'days_overdue',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'invoice_number',
            'gst_amount_cents',
            'total_amount_cents',
            'created_at',
            'updated_at',
        ]


class InvoiceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating invoices."""
    
    class Meta:
        model = Invoice
        fields = [
            'organization',
            'subscription',
            'subtotal_cents',
            'gst_rate',
            'iras_transaction_code',
            'currency',
            'due_date',
            'line_items',
            'stripe_invoice_id',
        ]
    
    def validate_subtotal_cents(self, value):
        """Ensure subtotal is positive."""
        if value <= 0:
            raise serializers.ValidationError('Subtotal must be positive.')
        return value


class InvoiceUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating invoices."""
    
    class Meta:
        model = Invoice
        fields = [
            'status',
            'due_date',
            'line_items',
            'metadata',
        ]


class MarkPaidSerializer(serializers.Serializer):
    """Serializer for marking invoice as paid."""
    
    payment_intent_id = serializers.CharField(required=False, allow_blank=True)
