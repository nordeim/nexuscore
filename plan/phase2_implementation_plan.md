# Phase 2: Infrastructure Models — Implementation Plan

## Goal

Create PRD-d-3 infrastructure models that MUST exist before any domain logic. These enable idempotency, audit logging, and webhook tracking.

---

## Proposed Changes

### Core App (`apps/core/`)

#### [NEW] [apps.py](file:///home/project/nexuscore/backend/apps/core/apps.py)
- CoreConfig app configuration

#### [NEW] [constants.py](file:///home/project/nexuscore/backend/apps/core/constants.py)
- SINGAPORE_TIMEZONE, DEFAULT_CURRENCY, GST_RATE, DSAR_SLA_HOURS

#### [NEW] [exceptions.py](file:///home/project/nexuscore/backend/apps/core/exceptions.py)
- IdempotencyConflict, RateLimitExceeded, UENValidationError

#### [NEW] [validators.py](file:///home/project/nexuscore/backend/apps/core/validators.py)
- UEN regex (ACRA formats), GST registration number regex

---

### Billing App (`apps/billing/`)

#### [NEW] [apps.py](file:///home/project/nexuscore/backend/apps/billing/apps.py)
- BillingConfig app configuration

#### [NEW] [models/__init__.py](file:///home/project/nexuscore/backend/apps/billing/models/__init__.py)
- Export IdempotencyRecord

#### [NEW] [models/idempotency.py](file:///home/project/nexuscore/backend/apps/billing/models/idempotency.py)
- IdempotencyRecord model with UUID PK, key, status, response caching

---

### Events App (`apps/events/`)

#### [NEW] [apps.py](file:///home/project/nexuscore/backend/apps/events/apps.py)
- EventsConfig app configuration

#### [NEW] [models.py](file:///home/project/nexuscore/backend/apps/events/models.py)
- Event model for audit logging (nullable FKs to User/Organization)

---

### Webhooks App (`apps/webhooks/`)

#### [NEW] [apps.py](file:///home/project/nexuscore/backend/apps/webhooks/apps.py)
- WebhooksConfig app configuration

#### [NEW] [models.py](file:///home/project/nexuscore/backend/apps/webhooks/models.py)
- WebhookEvent model with retry tracking

---

## File Count: 15 Files

| App | Files |
|-----|-------|
| core | 5 (__init__, apps, constants, exceptions, validators) |
| billing | 4 (__init__, apps, models/__init__, models/idempotency) |
| events | 3 (__init__, apps, models) |
| webhooks | 3 (__init__, apps, models) |

---

## Critical Dependencies

> ⚠️ Event model has ForeignKey to `users.User` and `organizations.Organization` which don't exist yet. We'll use string references that Django will resolve later.

---

## Verification Plan

```bash
# Update settings to include new apps
# Then run:
docker compose run --rm backend python manage.py makemigrations core billing events webhooks
docker compose run --rm backend python manage.py migrate

# Verify imports
docker compose run --rm backend python -c "
from apps.billing.models import IdempotencyRecord
from apps.events.models import Event
from apps.webhooks.models import WebhookEvent
print('✅ All models importable')
"
```

---

## Execution Order

1. Create core app structure (`__init__.py`, `apps.py`)
2. Create core utilities (constants, exceptions, validators)
3. Create billing app structure
4. Create IdempotencyRecord model
5. Create events app structure
6. Create Event model
7. Create webhooks app structure
8. Create WebhookEvent model
9. Update settings.py to include apps
10. Run makemigrations and migrate
11. Validate imports
