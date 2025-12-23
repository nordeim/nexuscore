"""
Billing Services
Business logic for invoice management
"""
from datetime import timedelta
from django.utils import timezone
from django.db import transaction

from apps.organizations.models import Organization

from .models import Invoice


class InvoiceService:
    """Service for invoice operations."""
    
    @staticmethod
    @transaction.atomic
    def create_invoice(
        organization: Organization,
        subtotal_cents: int,
        due_days: int = 30,
        stripe_invoice_id: str = None,
        **kwargs
    ) -> Invoice:
        """
        Create a new invoice with automatic GST calculation.
        
        Args:
            organization: Organization for the invoice
            subtotal_cents: Amount in cents before GST
            due_days: Days until due (default 30)
            stripe_invoice_id: Stripe invoice ID
            **kwargs: Additional invoice fields
            
        Returns:
            Invoice: Created invoice with GST calculated
        """
        import uuid
        
        invoice = Invoice.objects.create(
            organization=organization,
            subtotal_cents=subtotal_cents,
            due_date=timezone.now() + timedelta(days=due_days),
            stripe_invoice_id=stripe_invoice_id or f'inv_local_{uuid.uuid4().hex[:12]}',
            **kwargs
        )
        
        # Refresh to get GeneratedField values
        invoice.refresh_from_db()
        
        return invoice
    
    @staticmethod
    def mark_paid(invoice: Invoice, payment_intent_id: str = None) -> Invoice:
        """
        Mark an invoice as paid.
        
        Args:
            invoice: Invoice to mark as paid
            payment_intent_id: Stripe payment intent ID
            
        Returns:
            Invoice: Updated invoice
        """
        invoice.mark_paid(payment_intent_id)
        return invoice
    
    @staticmethod
    def void_invoice(invoice: Invoice) -> Invoice:
        """
        Void an invoice.
        
        Args:
            invoice: Invoice to void
            
        Returns:
            Invoice: Voided invoice
        """
        invoice.void()
        return invoice
    
    @staticmethod
    def get_organization_invoices(organization: Organization, status: str = None):
        """
        Get all invoices for an organization.
        
        Args:
            organization: Organization to get invoices for
            status: Optional status filter
            
        Returns:
            QuerySet: Matching invoices
        """
        qs = Invoice.objects.filter(organization=organization)
        if status:
            qs = qs.filter(status=status)
        return qs.order_by('-created_at')


class PDFService:
    """Service for PDF generation."""
    
    @staticmethod
    def generate_invoice_pdf(invoice: Invoice) -> str:
        """
        Generate PDF for an invoice.
        
        Args:
            invoice: Invoice to generate PDF for
            
        Returns:
            str: URL to the generated PDF
        """
        # TODO: Implement PDF generation with WeasyPrint or similar
        # Must include:
        # - Invoice number
        # - Organization details (UEN, GST reg no)
        # - IRAS transaction code
        # - Subtotal, GST breakdown, Total
        
        # For now, return a placeholder
        return f"https://storage.example.com/invoices/{invoice.id}.pdf"
    
    @staticmethod
    def upload_to_s3(pdf_content: bytes, filename: str) -> str:
        """
        Upload PDF to S3.
        
        Args:
            pdf_content: PDF file content
            filename: Filename to use
            
        Returns:
            str: S3 URL
        """
        # TODO: Implement S3 upload with boto3
        import uuid
        return f"https://s3.ap-southeast-1.amazonaws.com/invoices/{uuid.uuid4()}/{filename}"
