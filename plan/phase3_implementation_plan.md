# Phase 3: User & Authentication — Implementation Plan

## Goal

Create custom User model with email-based authentication, JWT tokens, and email verification.

---

## Proposed Changes

### Users App (`apps/users/`)

#### [NEW] [__init__.py](file:///home/project/nexuscore/backend/apps/users/__init__.py)
- Package init

#### [NEW] [apps.py](file:///home/project/nexuscore/backend/apps/users/apps.py)
- UsersConfig with ready() for signal registration

#### [NEW] [managers.py](file:///home/project/nexuscore/backend/apps/users/managers.py)
- UserManager with create_user/create_superuser

#### [NEW] [models.py](file:///home/project/nexuscore/backend/apps/users/models.py)
- User model with UUID PK, email as username
- Singapore timezone default
- Email verification fields

#### [NEW] [serializers.py](file:///home/project/nexuscore/backend/apps/users/serializers.py)
- UserSerializer, UserCreateSerializer, UserUpdateSerializer

#### [NEW] [views.py](file:///home/project/nexuscore/backend/apps/users/views.py)
- UserViewSet with /me endpoint
- RegisterView, VerifyEmailView

#### [NEW] [urls.py](file:///home/project/nexuscore/backend/apps/users/urls.py)
- Router + auth endpoints

#### [NEW] [signals.py](file:///home/project/nexuscore/backend/apps/users/signals.py)
- post_save signal for Event logging

#### [NEW] [tasks.py](file:///home/project/nexuscore/backend/apps/users/tasks.py)
- send_verification_email, send_welcome_email

#### [NEW] [admin.py](file:///home/project/nexuscore/backend/apps/users/admin.py)
- UserAdmin registration

---

## Settings Updates

1. Enable `AUTH_USER_MODEL = 'users.User'`
2. Add `'apps.users'` to `INSTALLED_APPS`
3. Update API URLs to include users app

---

## File Count: 10 Files

| Category | Files |
|----------|-------|
| Package | 2 (__init__.py, apps.py) |
| Models | 2 (managers.py, models.py) |
| API | 4 (serializers.py, views.py, urls.py, admin.py) |
| Background | 2 (signals.py, tasks.py) |

---

## Key Model Fields (User)

| Field | Type | Notes |
|-------|------|-------|
| id | UUID | Primary key |
| email | EmailField | Unique, USERNAME_FIELD |
| name | CharField | Required |
| timezone | CharField | default='Asia/Singapore' |
| is_verified | BooleanField | Email verification |
| verification_token | UUID | For email verification |

---

## Verification Plan

```bash
# Create migrations
uv run python manage.py makemigrations users
uv run python manage.py migrate

# Test superuser creation
uv run python manage.py createsuperuser --email admin@test.com

# Verify model
uv run python -c "from apps.users.models import User; print('✅ User model OK')"
```

---

## Execution Order

1. Create users app structure
2. Create managers.py
3. Create models.py with User
4. Enable AUTH_USER_MODEL in settings
5. Create migrations
6. Create serializers.py
7. Create views.py
8. Create urls.py
9. Create signals.py
10. Create tasks.py
11. Create admin.py
12. Update root urls.py
13. Migrate and validate
