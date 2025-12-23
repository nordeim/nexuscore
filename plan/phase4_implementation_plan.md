# Phase 4: Organization & Multi-tenancy — Implementation Plan

## Goal

Create Organization model with Singapore UEN/GST compliance and multi-tenant membership system.

---

## Proposed Changes

### Organizations App (`apps/organizations/`)

#### [NEW] [__init__.py](file:///home/project/nexuscore/backend/apps/organizations/__init__.py)
- Package init

#### [NEW] [apps.py](file:///home/project/nexuscore/backend/apps/organizations/apps.py)
- OrganizationsConfig

#### [NEW] [models.py](file:///home/project/nexuscore/backend/apps/organizations/models.py)
- **Organization** model with UEN/GST validation
- **OrganizationMembership** with roles

#### [NEW] [serializers.py](file:///home/project/nexuscore/backend/apps/organizations/serializers.py)
- OrganizationSerializer, OrganizationMembershipSerializer

#### [NEW] [views.py](file:///home/project/nexuscore/backend/apps/organizations/views.py)
- OrganizationViewSet with invite/remove member actions

#### [NEW] [urls.py](file:///home/project/nexuscore/backend/apps/organizations/urls.py)
- Router for organizations

#### [NEW] [permissions.py](file:///home/project/nexuscore/backend/apps/organizations/permissions.py)
- IsOrganizationMember, IsOrganizationAdmin, IsOrganizationOwner

#### [NEW] [admin.py](file:///home/project/nexuscore/backend/apps/organizations/admin.py)
- OrganizationAdmin, MembershipInline

---

## File Count: 8 Files

| Category | Files |
|----------|-------|
| Package | 2 (__init__.py, apps.py) |
| Models | 1 (models.py with 2 models) |
| API | 4 (serializers, views, urls, permissions) |
| Admin | 1 (admin.py) |

---

## Key Model Fields (Organization)

| Field | Type | Notes |
|-------|------|-------|
| `uen` | CharField | **Unique, ACRA regex** |
| `is_gst_registered` | Boolean | GST status |
| `gst_reg_no` | CharField | **IRAS regex: M+8digits+letter** |
| `timezone` | CharField | default='Asia/Singapore' |
| `locale` | CharField | default='en-SG' |

---

## UEN Validation (ACRA Singapore)

```python
UEN_REGEX = r'^[0-9]{8}[A-Z]$|^[0-9]{9}[A-Z]$|^[TSRQ][0-9]{2}[A-Z0-9]{4}[0-9]{3}[A-Z]$'
```

Valid formats:
- `12345678A` (8 digits + letter)
- `123456789A` (9 digits + letter)  
- `T12AB123A` (letter + 2 digits + 4 alphanum + 3 digits + letter)

---

## Verification Plan

```bash
uv run python manage.py makemigrations organizations
uv run python manage.py migrate

# Test UEN validation
uv run python -c "
from apps.organizations.models import Organization
from apps.users.models import User
user = User.objects.first()
org = Organization(name='Test', slug='test', uen='12345678A', billing_email='test@test.com', owner=user)
org.full_clean()
print('✅ UEN validation works')
"
```

---

## Execution Order

1. Create organizations app structure
2. Create models.py (Organization, OrganizationMembership)
3. Create permissions.py
4. Create serializers.py
5. Create views.py
6. Create urls.py
7. Create admin.py
8. Update settings.py
9. Update root urls.py
10. Migrate and validate
