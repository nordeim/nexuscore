# Phase 9: Webhooks & Integration — Implementation Plan

## Goal

Add Stripe webhook handling with signature verification and idempotency.

---

## Proposed Changes

### Webhooks App (`apps/webhooks/`) — Extend Existing

#### [NEW] [handlers/__init__.py](file:///home/project/nexuscore/backend/apps/webhooks/handlers/__init__.py)
- Handlers package

#### [NEW] [handlers/stripe.py](file:///home/project/nexuscore/backend/apps/webhooks/handlers/stripe.py)
- **StripeWebhookHandler** class

#### [NEW] [views.py](file:///home/project/nexuscore/backend/apps/webhooks/views.py)
- StripeWebhookView

#### [NEW] [urls.py](file:///home/project/nexuscore/backend/apps/webhooks/urls.py)
- Webhook endpoints

#### [NEW] [tasks.py](file:///home/project/nexuscore/backend/apps/webhooks/tasks.py)
- process_stripe_webhook task

#### [NEW] [admin.py](file:///home/project/nexuscore/backend/apps/webhooks/admin.py)
- WebhookEventAdmin

---

## File Count: 6 Files

---

## Key Features

| Feature | Implementation |
|---------|----------------|
| **Signature** | Stripe signature verification |
| **Deduplication** | Check event_id before processing |
| **Async** | Return 200, process via Celery |
| **Retry** | max_retries=3 with backoff |

---

## Handled Events

| Event | Handler |
|-------|---------|
| `invoice.paid` | handle_invoice_paid |
| `invoice.payment_failed` | handle_invoice_payment_failed |
| `customer.subscription.updated` | handle_subscription_updated |
| `customer.subscription.deleted` | handle_subscription_deleted |

---

## Verification Plan

```bash
# No new migrations needed (WebhookEvent exists)
uv run python manage.py check
```

---

## Execution Order

1. Create handlers/ package
2. Create handlers/stripe.py
3. Create views.py
4. Create urls.py
5. Create tasks.py
6. Create admin.py
7. Update root urls.py
