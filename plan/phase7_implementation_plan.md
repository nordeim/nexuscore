# Phase 7: Lead Management — Implementation Plan

## Goal

Create Lead model for marketing lead capture with UTM tracking and conversion tracking.

---

## Proposed Changes

### Leads App (`apps/leads/`)

#### [NEW] [__init__.py](file:///home/project/nexuscore/backend/apps/leads/__init__.py)
- Package init

#### [NEW] [apps.py](file:///home/project/nexuscore/backend/apps/leads/apps.py)
- LeadsConfig

#### [NEW] [models.py](file:///home/project/nexuscore/backend/apps/leads/models.py)
- **Lead** model with UTM fields

#### [NEW] [serializers.py](file:///home/project/nexuscore/backend/apps/leads/serializers.py)
- LeadSerializer

#### [NEW] [views.py](file:///home/project/nexuscore/backend/apps/leads/views.py)
- LeadViewSet

#### [NEW] [urls.py](file:///home/project/nexuscore/backend/apps/leads/urls.py)
- Router

#### [NEW] [admin.py](file:///home/project/nexuscore/backend/apps/leads/admin.py)
- LeadAdmin

---

## File Count: 7 Files

---

## Key Model Fields

| Field | Type | Notes |
|-------|------|-------|
| `source` | CharField | website/demo_request/contact/event/referral/other |
| `status` | CharField | new/contacted/qualified/converted/disqualified |
| `utm_source` | CharField | Google Analytics |
| `utm_medium` | CharField | Marketing tracking |
| `utm_campaign` | CharField | Campaign identifier |
| `assigned_to` | ForeignKey | Nullable user |
| `converted_to_user` | ForeignKey | Conversion tracking |

---

## Verification Plan

```bash
uv run python manage.py makemigrations leads
uv run python manage.py migrate
```

---

## Execution Order

1. Create leads app structure
2. Create models.py (Lead)
3. Create serializers.py
4. Create views.py
5. Create urls.py
6. Create admin.py
7. Update settings.py and root urls.py
8. Migrate and validate
