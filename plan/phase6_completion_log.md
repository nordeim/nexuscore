# Phase 6: Billing & GST Compliance — Walkthrough

**Completed**: 2025-12-23  
**Files Created**: 7

---

## Summary

Invoice model with Django 6.0 **GeneratedField** for database-level GST calculation.

---

## Key Files

| File | Purpose |
|------|---------|
| [invoice.py](file:///home/project/nexuscore/backend/apps/billing/models/invoice.py) | **GeneratedField for GST** |
| [serializers.py](file:///home/project/nexuscore/backend/apps/billing/serializers.py) | Invoice serializers |
| [views.py](file:///home/project/nexuscore/backend/apps/billing/views.py) | InvoiceViewSet |
| [services.py](file:///home/project/nexuscore/backend/apps/billing/services.py) | InvoiceService |
| [tasks.py](file:///home/project/nexuscore/backend/apps/billing/tasks.py) | Celery tasks |

---

## GST Implementation (Critical)

```python
# Database-level calculation
gst_amount_cents = GeneratedField(
    expression=Round(F('subtotal_cents') * F('gst_rate')),
    db_persist=True
)

total_amount_cents = GeneratedField(
    expression=F('subtotal_cents') + Round(F('subtotal_cents') * F('gst_rate')),
    db_persist=True
)
```

### IRAS Transaction Codes
| Code | Description |
|------|-------------|
| SR | Standard-Rated (9%) |
| ZR | Zero-Rated |
| OS | Out-of-Scope |
| TX | Exempted |

---

## Progress Summary

| Phase | Status | Tables |
|-------|--------|--------|
| Phase 1 | ✅ | - |
| Phase 2 | ✅ | 3 |
| Phase 3 | ✅ | 1 |
| Phase 4 | ✅ | 2 |
| Phase 5 | ✅ | 2 |
| Phase 6 | ✅ | 1 |
| **Total** | | **9 tables** |

---

## Next Steps

Phase 7 will create Lead Management for marketing lead capture.

---

# NexusCore v4.0 Implementation Tasks

## Current Objective
Phase 1: Project Foundation — Validation

## Task Checklist

### Phase: Master Execution Plan ✅ COMPLETE
- [x] Created Master Execution Plan (1,786 lines, 100 files)
- [x] Validated against PRD and PAD
- [x] Applied 6 corrections for alignment

### Phase 1: Project Foundation
- [x] **Implementation Planning** ✅ COMPLETE
  - [x] Review Phase 1 specs from Master Execution Plan
  - [x] Extract Docker config from PAD (lines 1048-1250)
  - [x] Create implementation_plan.md (12 files)
  - [x] User approval of plan
- [x] **Implementation Execution** ✅ COMPLETE
  - [x] Create docker-compose.yml (8 services)
  - [x] Create .env.example (Singapore region, PDPA)
  - [x] Create Makefile
  - [x] Create backend/Dockerfile
  - [x] Create backend/requirements/base.txt
  - [x] Create backend/requirements/development.txt
  - [x] Create backend/manage.py
  - [x] Create backend/config/__init__.py
  - [x] Create backend/config/celery.py
  - [x] Create backend/config/urls.py
  - [x] Create backend/config/settings/__init__.py
  - [x] Create backend/config/settings/base.py
  - [x] Create backend/config/settings/development.py
  - [x] Create infrastructure files (postgres, nginx)
  - [x] Create backend/apps/__init__.py
- [x] **Phase 1 Validation** ✅ COMPLETE
  - [x] docker compose config
  - [x] Verify file structure

### Phase 2: Infrastructure Models ✅ COMPLETE
- [x] **Implementation Planning**
  - [x] Review Phase 2 specs from Master Execution Plan
  - [x] Create implementation_plan.md (15 files)
  - [x] User approval of plan
- [x] **Implementation Execution**
  - [x] Create core app (constants, exceptions, validators)
  - [x] Create billing app + IdempotencyRecord model
  - [x] Create events app + Event model
  - [x] Create webhooks app + WebhookEvent model
  - [x] Update settings.py with new apps
- [x] **Phase 2 Validation** ✅ COMPLETE
  - [x] Fixed decouple import → get_env() helper
  - [x] Fixed CSP → django-csp 4.0 format
  - [x] Fixed Event ForeignKeys → UUIDFields
  - [x] Created migrations folders
  - [x] makemigrations billing events webhooks ✅
  - [x] migrate ✅ (3 tables created)

### Phase 3: User & Authentication ✅ COMPLETE
- [x] **Implementation Planning**
  - [x] Review Phase 3 specs from Master Execution Plan
  - [x] Create implementation_plan.md (10 files)
  - [x] User approval of plan
- [x] **Implementation Execution**
  - [x] Create users app structure
  - [x] Create managers.py + models.py
  - [x] Enable AUTH_USER_MODEL in settings
  - [x] Create serializers.py + views.py + urls.py
  - [x] Create signals.py + tasks.py + admin.py
  - [x] Update root urls.py
- [x] **Phase 3 Validation** ✅ COMPLETE
  - [x] Fixed CheckConstraint syntax (Django 6.0: condition= not check=)
  - [x] Reset database to fix migration history
  - [x] makemigrations users ✅
  - [x] migrate ✅ (users table created)

### Phase 4: Organization & Multi-tenancy ✅ COMPLETE
- [x] **Implementation Planning**
  - [x] Review Phase 4 specs from Master Execution Plan
  - [x] Create implementation_plan.md (8 files)
  - [x] User approval of plan
- [x] **Implementation Execution**
  - [x] Create organizations app structure
  - [x] Create models.py (Organization, OrganizationMembership)
  - [x] Create permissions.py, serializers.py, views.py
  - [x] Create urls.py, admin.py
  - [x] Update settings.py and root urls.py
- [x] **Phase 4 Validation** ✅ COMPLETE
  - [x] Fixed settings shadowing (org_timezone, org_settings)
  - [x] Fixed through_fields for ManyToMany
  - [x] Added django.contrib.postgres for ArrayField
  - [x] makemigrations organizations ✅
  - [x] migrate ✅ (2 tables created)

### Phase 5: Plans & Subscriptions ✅ COMPLETE
- [x] **Implementation Planning**
  - [x] Review Phase 5 specs from Master Execution Plan
  - [x] Create implementation_plan.md (9 files)
  - [x] User approval of plan
- [x] **Implementation Execution**
  - [x] Create subscriptions app structure
  - [x] Create models.py (Plan, Subscription)
  - [x] Create serializers.py, views.py, urls.py
  - [x] Create services.py, tasks.py, admin.py
  - [x] Update settings.py and root urls.py
- [x] **Phase 5 Validation** ✅ COMPLETE
  - [x] makemigrations subscriptions ✅
  - [x] migrate ✅ (2 tables created)

### Phase 6: Billing & GST Compliance ✅ COMPLETE
- [x] **Implementation Planning**
  - [x] Review Phase 6 specs from Master Execution Plan
  - [x] Create implementation_plan.md (7 files)
  - [x] User approval of plan
- [x] **Implementation Execution**
  - [x] Create Invoice model with GeneratedField
  - [x] Create serializers.py, views.py, urls.py
  - [x] Create services.py, tasks.py, admin.py
  - [x] Update root urls.py
- [x] **Phase 6 Validation** ✅ COMPLETE
  - [x] makemigrations billing ✅
  - [x] migrate ✅ (Invoice table created)

### Future Phases
- [ ] Phase 7: Lead Management
- [ ] Phase 8: PDPA & Privacy Compliance
- [ ] Phase 9: Webhooks & Integration
- [ ] Phase 10: Frontend Foundation
- [ ] Phase 11: Frontend Pages
- [ ] Phase 12: Testing & QA

