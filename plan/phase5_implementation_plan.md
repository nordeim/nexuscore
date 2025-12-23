# Phase 5: Plans & Subscriptions — Implementation Plan

## Goal

Create Plan and Subscription models with Stripe integration, idempotency handling, and SGD currency support.

---

## Proposed Changes

### Subscriptions App (`apps/subscriptions/`)

#### [NEW] [__init__.py](file:///home/project/nexuscore/backend/apps/subscriptions/__init__.py)
- Package init

#### [NEW] [apps.py](file:///home/project/nexuscore/backend/apps/subscriptions/apps.py)
- SubscriptionsConfig

#### [NEW] [models.py](file:///home/project/nexuscore/backend/apps/subscriptions/models.py)
- **Plan** model: SKU, pricing, Stripe IDs, features, limits
- **Subscription** model: status, period tracking, Stripe integration

#### [NEW] [serializers.py](file:///home/project/nexuscore/backend/apps/subscriptions/serializers.py)
- PlanSerializer, SubscriptionSerializer

#### [NEW] [views.py](file:///home/project/nexuscore/backend/apps/subscriptions/views.py)
- PlanViewSet (read-only), SubscriptionViewSet with idempotency

#### [NEW] [urls.py](file:///home/project/nexuscore/backend/apps/subscriptions/urls.py)
- Router for plans and subscriptions

#### [NEW] [services.py](file:///home/project/nexuscore/backend/apps/subscriptions/services.py)
- SubscriptionService for business logic

#### [NEW] [tasks.py](file:///home/project/nexuscore/backend/apps/subscriptions/tasks.py)
- Celery tasks for Stripe sync

#### [NEW] [admin.py](file:///home/project/nexuscore/backend/apps/subscriptions/admin.py)
- PlanAdmin, SubscriptionAdmin

---

## File Count: 9 Files

| Category | Files |
|----------|-------|
| Package | 2 (__init__.py, apps.py) |
| Models | 1 (models.py with 2 models) |
| API | 3 (serializers, views, urls) |
| Services | 2 (services.py, tasks.py) |
| Admin | 1 (admin.py) |

---

## Key Model Fields

### Plan
| Field | Type | Notes |
|-------|------|-------|
| `sku` | CharField | Unique identifier |
| `amount_cents` | PositiveIntegerField | Price in cents |
| `currency` | CharField | default='SGD' |
| `billing_period` | CharField | 'month' or 'year' |
| `stripe_price_id` | CharField | Stripe integration |

### Subscription
| Field | Type | Notes |
|-------|------|-------|
| `status` | CharField | trialing/active/canceled/etc |
| `current_period_start` | DateTimeField | Billing period |
| `stripe_subscription_id` | CharField | Unique Stripe ID |

---

## Critical Features

1. **Idempotency** → Check `Idempotency-Key` header on create
2. **Currency** → Default SGD for Singapore
3. **Stripe** → Store subscription/customer IDs
4. **Async** → Django 6.0 async cancel endpoint

---

## Verification Plan

```bash
uv run python manage.py makemigrations subscriptions
uv run python manage.py migrate

# Test Plan model
uv run python -c "
from apps.subscriptions.models import Plan
plan = Plan(name='Starter', sku='starter', billing_period='month', amount_cents=2999)
plan.full_clean()
print('✅ Plan model OK')
"
```

---

## Execution Order

1. Create subscriptions app structure
2. Create models.py (Plan, Subscription)
3. Create serializers.py
4. Create views.py with idempotency
5. Create urls.py
6. Create services.py
7. Create tasks.py
8. Create admin.py
9. Update settings.py and root urls.py
10. Migrate and validate
