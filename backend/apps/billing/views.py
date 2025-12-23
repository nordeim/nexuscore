"""
Billing Views
API endpoints for invoice management
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.events.models import Event

from .models import Invoice
from .serializers import (
    InvoiceSerializer,
    InvoiceCreateSerializer,
    InvoiceUpdateSerializer,
    MarkPaidSerializer,
)


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for invoice management.
    
    Endpoints:
    - GET /invoices/ - List user's invoices
    - POST /invoices/ - Create invoice
    - GET /invoices/{id}/ - Get invoice details
    - POST /invoices/{id}/mark-paid/ - Mark invoice as paid
    - POST /invoices/{id}/void/ - Void invoice
    """
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return invoices for user's organizations."""
        return Invoice.objects.filter(
            organization__memberships__user=self.request.user
        ).select_related('organization', 'subscription').distinct()
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return InvoiceCreateSerializer
        if self.action in ['update', 'partial_update']:
            return InvoiceUpdateSerializer
        return InvoiceSerializer
    
    @action(detail=True, methods=['post'], url_path='mark-paid')
    def mark_paid(self, request, pk=None):
        """
        Mark invoice as paid.
        
        POST /invoices/{id}/mark-paid/
        """
        invoice = self.get_object()
        
        if invoice.paid:
            return Response(
                {'error': 'Invoice is already paid.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = MarkPaidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        invoice.mark_paid(
            payment_intent_id=serializer.validated_data.get('payment_intent_id')
        )
        
        # Log event
        Event.log(
            event_type='invoice.paid',
            user_id=request.user.id,
            organization_id=invoice.organization_id,
            invoice_id=str(invoice.id),
            amount_cents=invoice.total_amount_cents,
        )
        
        return Response(InvoiceSerializer(invoice).data)
    
    @action(detail=True, methods=['post'])
    def void(self, request, pk=None):
        """
        Void an invoice.
        
        POST /invoices/{id}/void/
        """
        invoice = self.get_object()
        
        if invoice.status == 'paid':
            return Response(
                {'error': 'Cannot void a paid invoice.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if invoice.status == 'void':
            return Response(
                {'error': 'Invoice is already void.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        invoice.void()
        
        # Log event
        Event.log(
            event_type='invoice.voided',
            user_id=request.user.id,
            organization_id=invoice.organization_id,
            invoice_id=str(invoice.id),
        )
        
        return Response(InvoiceSerializer(invoice).data)
    
    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        """
        Get or generate invoice PDF.
        
        GET /invoices/{id}/pdf/
        """
        invoice = self.get_object()
        
        if invoice.pdf_url:
            return Response({'pdf_url': invoice.pdf_url})
        
        # Trigger PDF generation
        from .tasks import generate_invoice_pdf
        generate_invoice_pdf.delay(str(invoice.id))
        
        return Response(
            {'message': 'PDF generation queued.'},
            status=status.HTTP_202_ACCEPTED
        )
