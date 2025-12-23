"""
Billing Celery Tasks
Background tasks for invoice processing
"""
from celery import shared_task


@shared_task(queue='default')
def generate_invoice_pdf(invoice_id: str) -> dict:
    """
    Generate PDF for an invoice.
    
    Args:
        invoice_id: UUID of the invoice
        
    Returns:
        dict: Result with PDF URL
    """
    from .models import Invoice
    from .services import PDFService
    
    try:
        invoice = Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:
        return {'error': 'Invoice not found'}
    
    # Generate PDF
    pdf_url = PDFService.generate_invoice_pdf(invoice)
    
    # Update invoice with PDF URL
    invoice.pdf_url = pdf_url
    invoice.save(update_fields=['pdf_url', 'updated_at'])
    
    return {'status': 'success', 'pdf_url': pdf_url}


@shared_task(queue='high')
def process_invoice_payment(invoice_id: str, payment_intent_id: str) -> dict:
    """
    Process payment for an invoice.
    
    Args:
        invoice_id: UUID of the invoice
        payment_intent_id: Stripe payment intent ID
        
    Returns:
        dict: Processing result
    """
    from .models import Invoice
    from .services import InvoiceService
    
    try:
        invoice = Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:
        return {'error': 'Invoice not found'}
    
    if invoice.paid:
        return {'status': 'already_paid', 'invoice_id': str(invoice_id)}
    
    # Mark as paid
    InvoiceService.mark_paid(invoice, payment_intent_id)
    
    # Trigger follow-up tasks
    send_invoice_email.delay(str(invoice_id), template='payment_receipt')
    
    return {'status': 'paid', 'invoice_id': str(invoice_id)}


@shared_task(queue='default')
def send_invoice_email(invoice_id: str, template: str = 'invoice') -> dict:
    """
    Send invoice-related email.
    
    Args:
        invoice_id: UUID of the invoice
        template: Email template to use
        
    Returns:
        dict: Send result
    """
    from .models import Invoice
    
    try:
        invoice = Invoice.objects.select_related('organization').get(id=invoice_id)
    except Invoice.DoesNotExist:
        return {'error': 'Invoice not found'}
    
    # TODO: Implement email sending with SendGrid/SES
    # Templates:
    # - 'invoice': New invoice notification
    # - 'payment_receipt': Payment confirmation
    # - 'overdue_reminder': Overdue payment reminder
    
    return {
        'status': 'sent',
        'invoice_id': str(invoice_id),
        'template': template,
        'recipient': invoice.organization.billing_email
    }


@shared_task(queue='low')
def check_overdue_invoices() -> dict:
    """
    Check for overdue invoices and send reminders.
    
    Returns:
        dict: Count of processed invoices
    """
    from django.utils import timezone
    from .models import Invoice
    
    # Find overdue unpaid invoices
    overdue = Invoice.objects.filter(
        status='open',
        paid=False,
        due_date__lt=timezone.now()
    )
    
    count = 0
    for invoice in overdue:
        # Send reminder email
        send_invoice_email.delay(str(invoice.id), template='overdue_reminder')
        count += 1
    
    return {'processed': count}
