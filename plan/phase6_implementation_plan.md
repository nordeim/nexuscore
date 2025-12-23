# Phase 6: Billing & GST Compliance — Implementation Plan

## Goal

Create Invoice model with Django 6.0 GeneratedField for database-level GST calculation.

---

## Proposed Changes

### Billing App (`apps/billing/`) — Extend Existing

#### [MODIFY] [models.py](file:///home/project/nexuscore/backend/apps/billing/models.py)
- Add **Invoice** model with GeneratedField for GST
- Add **InvoiceLineItem** model

#### [NEW] [serializers.py](file:///home/project/nexuscore/backend/apps/billing/serializers.py)
- InvoiceSerializer, InvoiceLineItemSerializer

#### [NEW] [views.py](file:///home/project/nexuscore/backend/apps/billing/views.py)
- InvoiceViewSet

#### [NEW] [urls.py](file:///home/project/nexuscore/backend/apps/billing/urls.py)
- Router for invoices

#### [NEW] [services.py](file:///home/project/nexuscore/backend/apps/billing/services.py)
- InvoiceService, PDFService

#### [NEW] [tasks.py](file:///home/project/nexuscore/backend/apps/billing/tasks.py)
- generate_invoice_pdf, process_invoice_payment, send_invoice_email

#### [NEW] [admin.py](file:///home/project/nexuscore/backend/apps/billing/admin.py)
- InvoiceAdmin

---

## File Count: 6 New + 1 Modified = 7 Files

---

## Key Invoice Fields

| Field | Type | Notes |
|-------|------|-------|
| `subtotal_cents` | BigIntegerField | Base amount |
| `gst_rate` | DecimalField | **default=0.0900 (9%)** |
| `gst_amount_cents` | **GeneratedField** | `ROUND(subtotal * rate)` |
| `total_amount_cents` | **GeneratedField** | `subtotal + gst` |
| `iras_transaction_code` | CharField | SR/ZR/OS/TX |
| `currency` | CharField | **default='SGD'** |

---

## IRAS Transaction Codes

| Code | Description |
|------|-------------|
| `SR` | Standard-Rated (9% GST) |
| `ZR` | Zero-Rated |
| `OS` | Out-of-Scope |
| `TX` | Exempted |

---

## Verification Plan

```bash
uv run python manage.py makemigrations billing
uv run python manage.py migrate

# Test GST calculation
uv run python -c "
from apps.billing.models import Invoice
from apps.organizations.models import Organization
from django.utils import timezone
from datetime import timedelta

org = Organization.objects.first()
invoice = Invoice.objects.create(
    organization=org,
    subtotal_cents=10000,  # \$100
    due_date=timezone.now() + timedelta(days=30),
    stripe_invoice_id='inv_test123'
)
invoice.refresh_from_db()
print(f'GST: {invoice.gst_amount_cents}')  # Should be 900
print(f'Total: {invoice.total_amount_cents}')  # Should be 10900
assert invoice.gst_amount_cents == 900
print('✅ GST GeneratedField OK')
"
```

---

## Execution Order

1. Update billing/models.py with Invoice model
2. Create serializers.py
3. Create views.py
4. Create urls.py
5. Create services.py
6. Create tasks.py
7. Create admin.py
8. Update root urls.py
9. Migrate and validate GST calculation
