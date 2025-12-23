# Phase 8: PDPA & Privacy Compliance — Implementation Plan

## Goal

Create DSARRequest model with 72-hour SLA tracking and manual deletion approval.

---

## Proposed Changes

### Privacy App (`apps/privacy/`)

#### [NEW] [__init__.py](file:///home/project/nexuscore/backend/apps/privacy/__init__.py)
- Package init

#### [NEW] [apps.py](file:///home/project/nexuscore/backend/apps/privacy/apps.py)
- PrivacyConfig

#### [NEW] [models.py](file:///home/project/nexuscore/backend/apps/privacy/models.py)
- **DSARRequest** model with SLA tracking

#### [NEW] [serializers.py](file:///home/project/nexuscore/backend/apps/privacy/serializers.py)
- DSARRequestSerializer

#### [NEW] [views.py](file:///home/project/nexuscore/backend/apps/privacy/views.py)
- DSARRequestViewSet

#### [NEW] [urls.py](file:///home/project/nexuscore/backend/apps/privacy/urls.py)
- Router

#### [NEW] [tasks.py](file:///home/project/nexuscore/backend/apps/privacy/tasks.py)
- process_dsar_export, send_verification_email, enforce_pdpa_retention

#### [NEW] [admin.py](file:///home/project/nexuscore/backend/apps/privacy/admin.py)
- DSARRequestAdmin

---

## File Count: 8 Files

---

## Key Model Fields

| Field | Type | Notes |
|-------|------|-------|
| `request_type` | CharField | export/delete/access/rectification |
| `status` | CharField | pending/verifying/processing/completed/failed |
| `verification_token` | UUID | Email verification |
| `deletion_approved_by` | ForeignKey | **CRITICAL: Manual approval** |
| `sla_status` | property | 72-hour SLA tracking |

---

## SLA Logic (72 hours)

| Status | Condition |
|--------|-----------|
| `within_sla` | < 48 hours elapsed |
| `approaching_sla` | 48-72 hours elapsed |
| `breached_sla` | > 72 hours elapsed |
| `completed` | Request processed |

---

## Verification Plan

```bash
uv run python manage.py makemigrations privacy
uv run python manage.py migrate
```

---

## Execution Order

1. Create privacy app structure
2. Create models.py (DSARRequest)
3. Create serializers.py
4. Create views.py
5. Create urls.py
6. Create tasks.py
7. Create admin.py
8. Update settings.py and root urls.py
9. Migrate and validate
