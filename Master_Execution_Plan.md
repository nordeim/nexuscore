# NexusCore v4.0 — Master Execution Plan

> **Complete Codebase Implementation Guide for AI Coding Agents**  
> Version: 1.0.0 | Date: 2025-12-23 | Total Phases: 12

---

## Document Purpose

This Master Execution Plan provides **step-by-step instructions** for an AI coding agent to build the complete NexusCore v4.0 codebase. Each phase is **independently executable** with minimal supervision.

### Execution Protocol

1. Execute phases **in order** (dependencies are critical)
2. Create each file with its specified interface
3. Validate against the file's checklist before proceeding
4. Run phase validation before moving to the next phase

### Reference Documents

| Document | Purpose |
|----------|---------|
| `AGENT.md` | Project context and architecture briefing |
| `NexusCore-v4.0-Merged-PRD.md` | Complete technical specification |
| `Project_Architecture_Document.md` | C4 diagrams and implementation details |

---

## Phase Overview

| Phase | Name | Duration | Key Deliverables |
|-------|------|----------|------------------|
| 1 | Project Foundation | Week 1 | Django/Next.js scaffolding, Docker |
| 2 | Core Infrastructure Models | Week 1-2 | IdempotencyRecord, Event, WebhookEvent |
| 3 | User & Authentication | Week 2 | User model, auth endpoints, JWT |
| 4 | Organization & Multi-tenancy | Week 3 | Organization, Membership, UEN |
| 5 | Plans & Subscriptions | Week 4 | Plan, Subscription models |
| 6 | Billing & GST Compliance | Week 5-6 | Invoice with GeneratedField |
| 7 | Lead Management | Week 6 | Lead model and API |
| 8 | PDPA & Privacy | Week 7 | DSARRequest, retention tasks |
| 9 | Webhooks & Integration | Week 8-9 | Stripe handlers, Celery tasks |
| 10 | Frontend Foundation | Week 9-10 | Next.js setup, design system |
| 11 | Frontend Application | Week 10-11 | All pages and components |
| 12 | Testing & Production | Week 12-13 | Tests, security, deployment |

---

## PHASE 1: Project Foundation

**Duration**: Week 1 (Days 1-2)  
**Dependencies**: None  
**Objective**: Create project scaffolding and Docker environment

### Files to Create

#### 1.1 `docker-compose.yml`

**Purpose**: Define all development services  
**Location**: `/nexuscore/docker-compose.yml`

**Interface**:
```yaml
services:
  - nginx (port 80, 443)
  - backend (port 8000)
  - frontend (port 3000)
  - celery (worker)
  - postgres (port 5432)
  - redis (port 6379)
  - mailpit (port 8025, 1025)
```

**Validation Checklist**:
- [ ] PostgreSQL version is 16+
- [ ] Redis version is 7.4
- [ ] All services have health checks
- [ ] Volumes defined for postgres data
- [ ] Network `nexuscore-network` created
- [ ] Environment variables loaded from `.env`

---

#### 1.2 `.env.example`

**Purpose**: Document all required environment variables  
**Location**: `/nexuscore/.env.example`

**Interface**:
```bash
# Required sections:
# - APPLICATION (DEBUG, SECRET_KEY, ALLOWED_HOSTS)
# - DATABASE (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
# - REDIS (REDIS_URL, CELERY_BROKER_URL)
# - AWS (AWS_S3_REGION_NAME=ap-southeast-1)
# - STRIPE (STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET)
# - EMAIL (EMAIL_HOST, SENDGRID_API_KEY)
# - SENTRY
# - FRONTEND (NEXT_PUBLIC_*)
# - SECURITY
# - FEATURE FLAGS (PDPA_DSAR_SLA_HOURS=72)
```

**Validation Checklist**:
- [ ] AWS_S3_REGION_NAME set to `ap-southeast-1`
- [ ] CELERY_TIMEZONE set to `Asia/Singapore`
- [ ] PDPA_DSAR_SLA_HOURS set to 72
- [ ] All Stripe variables documented
- [ ] Comments explain each variable

---

#### 1.3 `backend/Dockerfile`

**Purpose**: Django application container  
**Location**: `/nexuscore/backend/Dockerfile`

**Interface**:
```dockerfile
FROM python:3.12-slim
# Install dependencies
# Copy requirements
# Set working directory /app
# Expose port 8000
```

**Validation Checklist**:
- [ ] Python version 3.12+
- [ ] Non-root user created
- [ ] Requirements installed from requirements/
- [ ] PYTHONDONTWRITEBYTECODE=1
- [ ] PYTHONUNBUFFERED=1

---

#### 1.4 `backend/requirements/base.txt`

**Purpose**: Core Python dependencies  
**Location**: `/nexuscore/backend/requirements/base.txt`

**Interface**:
```
Django>=6.0,<7.0
djangorestframework>=3.15
psycopg[binary]>=3.1
redis>=5.0
celery>=5.4
stripe>=8.0
boto3>=1.34
```

**Validation Checklist**:
- [ ] Django 6.0+ specified
- [ ] psycopg3 (not psycopg2)
- [ ] All versions pinned with minimum
- [ ] No conflicting dependencies

---

#### 1.5 `backend/manage.py`

**Purpose**: Django management script  
**Location**: `/nexuscore/backend/manage.py`

**Validation Checklist**:
- [ ] Settings module set to `config.settings`
- [ ] Standard Django boilerplate

---

#### 1.6 `backend/config/__init__.py`

**Purpose**: Package initialization with Celery  
**Location**: `/nexuscore/backend/config/__init__.py`

**Interface**:
```python
from .celery import app as celery_app
__all__ = ('celery_app',)
```

**Validation Checklist**:
- [ ] Celery app imported and exported

---

#### 1.7 `backend/config/settings/base.py`

**Purpose**: Shared Django settings  
**Location**: `/nexuscore/backend/config/settings/base.py`

**Interface**:
```python
# Required configurations:
# - INSTALLED_APPS with custom apps
# - DATABASES with CONN_HEALTH_CHECKS=True
# - MIDDLEWARE with CSP
# - AUTH_USER_MODEL = 'users.User'
# - REST_FRAMEWORK configuration
# - CELERY configuration
# - AWS S3 configuration
```

**Validation Checklist**:
- [ ] CONN_HEALTH_CHECKS = True
- [ ] AUTH_USER_MODEL = 'users.User'
- [ ] TIME_ZONE = 'Asia/Singapore'
- [ ] LANGUAGE_CODE = 'en-sg'
- [ ] CSP middleware included
- [ ] Celery broker configured

---

#### 1.8 `backend/config/celery.py`

**Purpose**: Celery application configuration  
**Location**: `/nexuscore/backend/config/celery.py`

**Interface**:
```python
app = Celery('nexuscore')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Task queues: high, default, low
```

**Validation Checklist**:
- [ ] Three queues defined (high, default, low)
- [ ] Task autodiscovery enabled
- [ ] Timezone set to Asia/Singapore

---

#### 1.9 `backend/config/urls.py`

**Purpose**: Root URL configuration  
**Location**: `/nexuscore/backend/config/urls.py`

**Interface**:
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.api.urls')),
    path('health/', health_check_view),
]
```

**Validation Checklist**:
- [ ] Admin enabled
- [ ] API versioned at /api/v1/
- [ ] Health check endpoint exists

---

### Phase 1 Validation

Run these commands to validate Phase 1:
```bash
docker-compose config  # Validates docker-compose.yml
docker-compose build   # Builds all images
docker-compose up -d postgres redis  # Starts dependencies
docker-compose run --rm backend python manage.py check  # Django check
```

**Success Criteria**:
- [ ] All containers build without errors
- [ ] PostgreSQL accepts connections
- [ ] Redis responds to PING
- [ ] Django settings load without errors

---

## PHASE 2: Infrastructure Models & Core Utilities

**Duration**: Week 1-2 (Days 3-5)  
**Dependencies**: Phase 1  
**Objective**: Implement PRD-d-3 infrastructure models per PAD structure

> ⚠️ **CRITICAL**: These models MUST exist before any domain logic
>
> **Note**: Per PAD Section 5.1, models are organized by app:
> - `IdempotencyRecord` → `apps/billing/`
> - `Event` → `apps/events/`
> - `WebhookEvent` → `apps/webhooks/`

### Files to Create

#### 2.1 `backend/apps/__init__.py`

**Purpose**: Apps package  
**Location**: `/nexuscore/backend/apps/__init__.py`

**Validation Checklist**:
- [ ] Empty file exists

---

#### 2.2 `backend/apps/core/__init__.py`

**Purpose**: Core app package  
**Location**: `/nexuscore/backend/apps/core/__init__.py`

**Validation Checklist**:
- [ ] Empty file exists

---

#### 2.3 `backend/apps/core/apps.py`

**Purpose**: Core app configuration  
**Location**: `/nexuscore/backend/apps/core/apps.py`

**Interface**:
```python
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
```

**Validation Checklist**:
- [ ] AppConfig subclass
- [ ] name = 'apps.core'

---

#### 2.4 `backend/apps/core/constants.py`

**Purpose**: Shared constants across apps  
**Location**: `/nexuscore/backend/apps/core/constants.py`

**Validation Checklist**:
- [ ] SINGAPORE_TIMEZONE = 'Asia/Singapore'
- [ ] DEFAULT_CURRENCY = 'SGD'
- [ ] GST_RATE = Decimal('0.0900')
- [ ] DSAR_SLA_HOURS = 72

---

#### 2.5 `backend/apps/core/exceptions.py`

**Purpose**: Custom exception classes  
**Location**: `/nexuscore/backend/apps/core/exceptions.py`

**Validation Checklist**:
- [ ] IdempotencyConflict exception
- [ ] RateLimitExceeded exception
- [ ] UENValidationError exception

---

#### 2.6 `backend/apps/core/validators.py`

**Purpose**: Reusable validators  
**Location**: `/nexuscore/backend/apps/core/validators.py`

**Interface**:
```python
UEN_REGEX = r'^[0-9]{8}[A-Z]$|^[0-9]{9}[A-Z]$|^[TSRQ][0-9]{2}[A-Z0-9]{4}[0-9]{3}[A-Z]$'
GST_REG_NO_REGEX = r'^M[0-9]{8}[A-Z]$'

def validate_uen(value: str) -> None
def validate_gst_reg_no(value: str) -> None
```

**Validation Checklist**:
- [ ] UEN regex matches ACRA formats
- [ ] GST regex matches IRAS format

---

#### 2.7 `backend/apps/billing/models/idempotency.py`

**Purpose**: Prevent duplicate operations (PRD-d-3)  
**Location**: `/nexuscore/backend/apps/billing/models/idempotency.py`

> **Per PAD Line 789**: IdempotencyRecord belongs in billing app

**Interface**:
```python
class IdempotencyRecord(models.Model):
    id = UUIDField(primary_key=True)
    key = CharField(max_length=255, unique=True)
    request_path = CharField(max_length=255)
    request_method = CharField(max_length=10)
    request_hash = CharField(max_length=64)  # SHA256
    status = CharField(choices=['processing', 'completed', 'failed'])
    response_status_code = IntegerField(null=True)
    response_body = JSONField(null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    expires_at = DateTimeField()
    
    def is_expired(self) -> bool
    
    class Meta:
        db_table = 'idempotency_records'
        indexes = [key, expires_at, (request_path, request_method)]
```

**Validation Checklist**:
- [ ] UUID primary key
- [ ] key field is unique with index
- [ ] status choices match spec
- [ ] is_expired() method implemented
- [ ] Three indexes created
- [ ] db_table = 'idempotency_records'

---

#### 2.8 `backend/apps/events/models.py`

**Purpose**: Audit logging for all mutations  
**Location**: `/nexuscore/backend/apps/events/models.py`

> **Per PAD Lines 548-556**: Event model has its own app

**Interface**:
```python
class Event(models.Model):
    id = UUIDField(primary_key=True)
    event_type = CharField(max_length=100, db_index=True)
    user = ForeignKey('users.User', null=True, on_delete=SET_NULL)
    organization = ForeignKey('organizations.Organization', null=True, on_delete=SET_NULL)
    data = JSONField(default=dict)
    created_at = DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'events'
        ordering = ['-created_at']
```

**Validation Checklist**:
- [ ] UUID primary key
- [ ] event_type indexed
- [ ] Nullable FK to User
- [ ] Nullable FK to Organization
- [ ] JSONField for data
- [ ] Ordered by -created_at

---

#### 2.9 `backend/apps/webhooks/models.py`

**Purpose**: Track external webhook events  
**Location**: `/nexuscore/backend/apps/webhooks/models.py`

> **Per PAD Lines 534-546**: WebhookEvent has its own app with handlers

**Interface**:
```python
class WebhookEvent(models.Model):
    id = UUIDField(primary_key=True)
    service = CharField(max_length=50)  # 'stripe', 'sendgrid'
    event_id = CharField(max_length=255, unique=True)
    event_type = CharField(max_length=100)
    payload = JSONField()
    processed = BooleanField(default=False)
    processing_error = TextField(blank=True)
    retry_count = PositiveIntegerField(default=0)
    last_retry_at = DateTimeField(null=True)
    created_at = DateTimeField(auto_now_add=True)
    processed_at = DateTimeField(null=True)
    
    class Meta:
        db_table = 'webhook_events'
        ordering = ['-created_at']
```

**Validation Checklist**:
- [ ] UUID primary key
- [ ] event_id is unique
- [ ] Retry tracking fields present
- [ ] processed_at nullable
- [ ] db_table = 'webhook_events'

---

#### 2.8 `backend/apps/core/admin.py`

**Purpose**: Admin registration for core models  
**Location**: `/nexuscore/backend/apps/core/admin.py`

**Validation Checklist**:
- [ ] IdempotencyRecord registered
- [ ] Event registered with list_filter on event_type
- [ ] WebhookEvent registered with list_filter on service, processed

---

### Phase 2 Validation

```bash
# Create migrations for all infrastructure apps
docker-compose run --rm backend python manage.py makemigrations billing events webhooks
docker-compose run --rm backend python manage.py migrate

# Verify models are importable from correct locations
docker-compose run --rm backend python manage.py shell -c "
from apps.billing.models import IdempotencyRecord
from apps.events.models import Event
from apps.webhooks.models import WebhookEvent
print('All infrastructure models OK')
"
```

**Success Criteria**:
- [ ] Migrations create without errors
- [ ] IdempotencyRecord importable from `apps.billing.models`
- [ ] Event importable from `apps.events.models`
- [ ] WebhookEvent importable from `apps.webhooks.models`
- [ ] Tables created in PostgreSQL

---

## PHASE 3: User & Authentication

**Duration**: Week 2  
**Dependencies**: Phase 2  
**Objective**: Custom User model with authentication

### Files to Create

#### 3.1 `backend/apps/users/__init__.py`

**Validation Checklist**:
- [ ] Empty file exists

---

#### 3.2 `backend/apps/users/apps.py`

**Interface**:
```python
class UsersConfig(AppConfig):
    name = 'apps.users'
```

**Validation Checklist**:
- [ ] name = 'apps.users'

---

#### 3.3 `backend/apps/users/models.py`

**Purpose**: Custom User with UUID primary key  
**Location**: `/nexuscore/backend/apps/users/models.py`

**Interface**:
```python
class UserManager(BaseUserManager):
    def create_user(email, password=None, **extra_fields)
    def create_superuser(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = UUIDField(primary_key=True)
    email = EmailField(unique=True)
    name = CharField(max_length=255)
    company = CharField(max_length=255, blank=True)
    phone = CharField(max_length=20, blank=True)
    is_verified = BooleanField(default=False)
    verification_token = UUIDField()
    verification_sent_at = DateTimeField(null=True)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    last_login = DateTimeField(null=True)
    timezone = CharField(default='Asia/Singapore')
    email_preferences = JSONField(default=dict)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        db_table = 'users'
        constraints = [verified_users_must_be_active]
```

**Validation Checklist**:
- [ ] UUID primary key
- [ ] Email is unique
- [ ] USERNAME_FIELD = 'email'
- [ ] timezone default = 'Asia/Singapore'
- [ ] UserManager with create_user/create_superuser
- [ ] db_table = 'users'
- [ ] CheckConstraint for verified_users_must_be_active

---

#### 3.4 `backend/apps/users/serializers.py`

**Purpose**: User serialization  
**Location**: `/nexuscore/backend/apps/users/serializers.py`

**Interface**:
```python
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'company', 'phone', 'timezone', 'is_verified', 'created_at']
        read_only_fields = ['id', 'is_verified', 'created_at']

class UserCreateSerializer(ModelSerializer):
    password = CharField(write_only=True, min_length=8)
    
class UserUpdateSerializer(ModelSerializer):
    # Partial update support
```

**Validation Checklist**:
- [ ] Password write_only
- [ ] id read_only
- [ ] Email validation
- [ ] Separate create/update serializers

---

#### 3.5 `backend/apps/users/views.py`

**Purpose**: User API views  
**Location**: `/nexuscore/backend/apps/users/views.py`

**Interface**:
```python
class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return only current user's data
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        # Return current user

class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    # Verify email with token
```

**Validation Checklist**:
- [ ] /me endpoint returns current user
- [ ] Register is public (AllowAny)
- [ ] Email verification endpoint

---

#### 3.6 `backend/apps/users/urls.py`

**Purpose**: User URL routing  
**Location**: `/nexuscore/backend/apps/users/urls.py`

**Interface**:
```python
router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('verify/<uuid:token>/', VerifyEmailView.as_view()),
]
```

**Validation Checklist**:
- [ ] Router for UserViewSet
- [ ] Register endpoint
- [ ] Verify endpoint with UUID token

---

#### 3.7 `backend/apps/users/managers.py`

**Purpose**: Custom User manager  
**Location**: `/nexuscore/backend/apps/users/managers.py`

> **Per PAD Line 470**: Separate managers file

**Interface**:
```python
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields) -> User
    def create_superuser(self, email, password, **extra_fields) -> User
    def get_by_natural_key(self, email) -> User
```

**Validation Checklist**:
- [ ] create_user normalizes email
- [ ] create_superuser sets is_staff=True, is_superuser=True
- [ ] Email is lowercased

---

#### 3.8 `backend/apps/users/signals.py`

**Purpose**: User-related Django signals  
**Location**: `/nexuscore/backend/apps/users/signals.py`

> **Per PAD Line 474**: Separate signals file

**Interface**:
```python
@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, **kwargs):
    if created:
        Event.objects.create(
            event_type='user.created',
            user=instance,
            data={'email': instance.email}
        )
```

**Validation Checklist**:
- [ ] post_save signal for user creation
- [ ] Creates Event for audit log
- [ ] Connected in apps.py ready() method

---

#### 3.9 `backend/apps/users/tasks.py`

**Purpose**: User-related async tasks  
**Location**: `/nexuscore/backend/apps/users/tasks.py`

**Interface**:
```python
@shared_task(queue='default')
def send_verification_email(user_id: str) -> None

@shared_task(queue='default')
def send_welcome_email(user_id: str) -> None

@shared_task(queue='default')
def send_password_reset_email(user_id: str, token: str) -> None
```

**Validation Checklist**:
- [ ] All tasks use @shared_task
- [ ] queue='default' specified
- [ ] Type hints present

---

### Phase 3 Validation

```bash
docker-compose run --rm backend python manage.py makemigrations users
docker-compose run --rm backend python manage.py migrate
docker-compose run --rm backend python manage.py createsuperuser --email admin@test.com --noinput
docker-compose run --rm backend python manage.py test apps.users
```

**Success Criteria**:
- [ ] User model migrates successfully
- [ ] Superuser can be created
- [ ] AUTH_USER_MODEL works

---

## PHASE 4: Organization & Multi-tenancy

**Duration**: Week 3  
**Dependencies**: Phase 3  
**Objective**: Organization with Singapore UEN/GST compliance

### Files to Create

#### 4.1 `backend/apps/organizations/models.py`

**Purpose**: Organization with Singapore compliance  
**Location**: `/nexuscore/backend/apps/organizations/models.py`

**Interface**:
```python
class Organization(models.Model):
    id = UUIDField(primary_key=True)
    name = CharField(max_length=255)
    slug = SlugField(max_length=100, unique=True)
    
    # Singapore Compliance - CRITICAL
    uen = CharField(
        max_length=15, unique=True,
        validators=[RegexValidator(
            regex=r'^[0-9]{8}[A-Z]$|^[0-9]{9}[A-Z]$|^[TSRQ][0-9]{2}[A-Z0-9]{4}[0-9]{3}[A-Z]$'
        )]
    )
    is_gst_registered = BooleanField(default=False)
    gst_reg_no = CharField(
        max_length=20, blank=True, null=True,
        validators=[RegexValidator(regex=r'^M[0-9]{8}[A-Z]$')]
    )
    
    # Billing
    stripe_customer_id = CharField(max_length=255, blank=True)
    billing_email = EmailField()
    billing_phone = CharField(max_length=20, blank=True)
    billing_address = JSONField(default=dict)
    
    # Settings
    timezone = CharField(default='Asia/Singapore')
    locale = CharField(default='en-SG')
    settings = JSONField(default=dict)
    
    # Relationships
    owner = ForeignKey(User, on_delete=PROTECT, related_name='owned_organizations')
    members = ManyToManyField(User, through='OrganizationMembership')
    
    # Timestamps
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    trial_ends_at = DateTimeField(null=True)
    
    @property
    def is_in_trial(self) -> bool
    
    @property
    def days_left_in_trial(self) -> int
    
    class Meta:
        db_table = 'organizations'
        constraints = [
            trial_ends_after_creation,
            valid_gst_registration  # if is_gst_registered, gst_reg_no required
        ]

class OrganizationMembership(models.Model):
    id = UUIDField(primary_key=True)
    organization = ForeignKey(Organization, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    role = CharField(choices=['owner', 'admin', 'member', 'viewer'])
    permissions = ArrayField(CharField(max_length=50), default=list)
    joined_at = DateTimeField(auto_now_add=True)
    invited_by = ForeignKey(User, null=True, on_delete=SET_NULL)
    
    class Meta:
        db_table = 'organization_memberships'
        unique_together = [('organization', 'user')]
```

**Validation Checklist**:
- [ ] UEN regex matches ACRA formats (3 patterns)
- [ ] GST registration number regex: ^M[0-9]{8}[A-Z]$
- [ ] timezone default 'Asia/Singapore'
- [ ] locale default 'en-SG'
- [ ] valid_gst_registration constraint
- [ ] OrganizationMembership with ArrayField for permissions
- [ ] unique_together on (organization, user)

---

#### 4.2 `backend/apps/organizations/serializers.py`

**Validation Checklist**:
- [ ] OrganizationSerializer with UEN validation
- [ ] OrganizationMembershipSerializer
- [ ] Nested members in OrganizationDetailSerializer

---

#### 4.3 `backend/apps/organizations/views.py`

**Validation Checklist**:
- [ ] OrganizationViewSet with permission checking
- [ ] @action for invite_member
- [ ] @action for remove_member
- [ ] UEN validation error messages

---

#### 4.4 `backend/apps/organizations/permissions.py`

**Interface**:
```python
class IsOrganizationMember(BasePermission):
    def has_object_permission(self, request, view, obj)

class IsOrganizationAdmin(BasePermission):
    def has_object_permission(self, request, view, obj)

class IsOrganizationOwner(BasePermission):
    def has_object_permission(self, request, view, obj)
```

**Validation Checklist**:
- [ ] Three permission classes
- [ ] Check membership role appropriately

---

### Phase 4 Validation

```bash
docker-compose run --rm backend python manage.py makemigrations organizations
docker-compose run --rm backend python manage.py migrate
docker-compose run --rm backend python manage.py shell << 'EOF'
from apps.organizations.models import Organization
from apps.users.models import User
user = User.objects.first()
# Test valid UEN
org = Organization(name='Test', slug='test', uen='12345678A', billing_email='test@test.com', owner=user)
org.full_clean()  # Should pass
print('Valid UEN: OK')
# Test invalid UEN
try:
    org2 = Organization(name='Test2', slug='test2', uen='INVALID', billing_email='test@test.com', owner=user)
    org2.full_clean()
except Exception as e:
    print(f'Invalid UEN rejected: OK')
EOF
```

**Success Criteria**:
- [ ] Valid UEN formats accepted
- [ ] Invalid UEN formats rejected
- [ ] GST constraint works

---

## PHASE 5: Plans & Subscriptions

**Duration**: Week 4  
**Dependencies**: Phase 4  
**Objective**: Subscription management with idempotency

### Files to Create

#### 5.1 `backend/apps/subscriptions/models.py`

**Interface**:
```python
class Plan(models.Model):
    id = UUIDField(primary_key=True)
    name = CharField(max_length=100)
    description = TextField(blank=True)
    sku = CharField(max_length=50, unique=True)
    billing_period = CharField(choices=['month', 'year'])
    amount_cents = PositiveIntegerField()
    currency = CharField(default='SGD')
    features = JSONField(default=dict)
    limits = JSONField(default=dict)
    is_active = BooleanField(default=True)
    is_visible = BooleanField(default=True)
    display_order = PositiveIntegerField(default=0)
    stripe_price_id = CharField(max_length=255, blank=True)
    stripe_product_id = CharField(max_length=255, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    @property
    def amount_dollars(self) -> float
    
    class Meta:
        db_table = 'plans'
        ordering = ['display_order', 'created_at']

class Subscription(models.Model):
    id = UUIDField(primary_key=True)
    organization = ForeignKey(Organization, on_delete=PROTECT)
    plan = ForeignKey(Plan, on_delete=PROTECT)
    status = CharField(choices=['trialing', 'active', 'past_due', 'canceled', 'unpaid'])
    cancel_at_period_end = BooleanField(default=False)
    current_period_start = DateTimeField()
    current_period_end = DateTimeField()
    trial_start = DateTimeField(null=True)
    trial_end = DateTimeField(null=True)
    stripe_subscription_id = CharField(max_length=255, unique=True)
    stripe_customer_id = CharField(max_length=255)
    stripe_latest_invoice_id = CharField(max_length=255, blank=True)
    metadata = JSONField(default=dict)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    canceled_at = DateTimeField(null=True)
    
    @property
    def is_active(self) -> bool
    
    @property
    def is_in_trial(self) -> bool
    
    class Meta:
        db_table = 'subscriptions'
        constraints = [
            period_end_after_start,
            trial_status_requires_trial_end
        ]
        indexes = [
            Index(fields=['organization'], condition=Q(status__in=['active', 'trialing']), name='idx_active_subscriptions')
        ]
```

**Validation Checklist**:
- [ ] currency default 'SGD'
- [ ] Partial index for active subscriptions
- [ ] period_end_after_start constraint
- [ ] trial_status_requires_trial_end constraint

---

#### 5.2 `backend/apps/subscriptions/views.py`

**Interface**:
```python
class SubscriptionViewSet(ModelViewSet):
    @transaction.atomic
    def create(self, request):
        # CRITICAL: Idempotency key handling
        idempotency_key = request.headers.get('Idempotency-Key')
        if not idempotency_key:
            return Response({'error': 'Idempotency-Key required'}, status=400)
        
        # Check IdempotencyRecord
        # Create subscription
        # Enqueue Stripe task
        # Log Event
    
    @action(detail=True, methods=['post'])
    async def cancel(self, request, pk=None):
        # Django 6.0 async
        subscription = await Subscription.objects.aget(id=pk)
        await subscription.asave()
```

**Validation Checklist**:
- [ ] Idempotency-Key header required
- [ ] IdempotencyRecord created/checked
- [ ] @transaction.atomic on create
- [ ] Async cancel with aget/asave
- [ ] Event logged on create

---

### Phase 5 Validation

```bash
docker-compose run --rm backend python manage.py makemigrations subscriptions
docker-compose run --rm backend python manage.py migrate
docker-compose run --rm backend python manage.py test apps.subscriptions
```

**Success Criteria**:
- [ ] Plan model created
- [ ] Subscription model created with constraints
- [ ] Idempotency check works

---

## PHASE 6: Billing & GST Compliance

**Duration**: Week 5-6  
**Dependencies**: Phase 5  
**Objective**: Invoice with database-level GST calculation

### Files to Create

#### 6.1 `backend/apps/billing/models.py`

**Purpose**: GST-compliant Invoice model  
**Location**: `/nexuscore/backend/apps/billing/models.py`

**Interface**:
```python
class Invoice(models.Model):
    id = UUIDField(primary_key=True)
    organization = ForeignKey(Organization, on_delete=PROTECT)
    subscription = ForeignKey(Subscription, null=True, on_delete=PROTECT)
    
    # GST Calculation - CRITICAL
    subtotal_cents = BigIntegerField()
    gst_rate = DecimalField(max_digits=5, decimal_places=4, default=0.0900)
    
    # DJANGO 6.0 GeneratedField
    gst_amount_cents = GeneratedField(
        expression=Func(F('subtotal_cents') * F('gst_rate'), function='ROUND', output_field=BigIntegerField()),
        output_field=BigIntegerField(),
        db_persist=True
    )
    
    total_amount_cents = GeneratedField(
        expression=F('subtotal_cents') + F('gst_amount_cents'),
        output_field=BigIntegerField(),
        db_persist=True
    )
    
    # IRAS compliance
    iras_transaction_code = CharField(choices=['SR', 'ZR', 'OS', 'TX'], default='SR')
    
    # Payment tracking
    amount_paid_cents = PositiveIntegerField(default=0)
    currency = CharField(default='SGD')
    status = CharField(choices=['draft', 'open', 'paid', 'void', 'uncollectible'])
    paid = BooleanField(default=False)
    due_date = DateTimeField()
    paid_at = DateTimeField(null=True)
    
    # Stripe
    stripe_invoice_id = CharField(max_length=255, unique=True)
    stripe_payment_intent_id = CharField(max_length=255, blank=True)
    
    # Data
    pdf_url = URLField(blank=True)
    line_items = JSONField(default=list)
    metadata = JSONField(default=dict)
    created_at = DateTimeField(auto_now_add=True)
    
    @property
    def is_overdue(self) -> bool
    
    @property
    def days_overdue(self) -> int
    
    class Meta:
        db_table = 'invoices'
        constraints = [
            amount_paid_not_exceed_due,
            paid_invoices_require_paid_at
        ]
```

**Validation Checklist**:
- [ ] gst_amount_cents is GeneratedField with ROUND
- [ ] total_amount_cents is GeneratedField
- [ ] db_persist=True on both
- [ ] gst_rate default 0.0900 (9%)
- [ ] iras_transaction_code with 4 choices
- [ ] currency default 'SGD'
- [ ] amount_paid_not_exceed_due constraint

---

#### 6.2 `backend/apps/billing/services.py`

**Interface**:
```python
class InvoiceService:
    @staticmethod
    def create_invoice(organization: Organization, subtotal_cents: int, **kwargs) -> Invoice
    
    @staticmethod
    def mark_paid(invoice: Invoice, payment_intent_id: str) -> Invoice
    
    @staticmethod
    def void_invoice(invoice: Invoice) -> Invoice

class PDFService:
    @staticmethod
    def generate_invoice_pdf(invoice: Invoice) -> str:
        # Returns S3 URL
        # Must include IRAS transaction code
```

**Validation Checklist**:
- [ ] Invoice creation with GST auto-calculation
- [ ] PDF includes IRAS transaction code
- [ ] PDF uploaded to S3

---

#### 6.3 `backend/apps/billing/tasks.py`

**Interface**:
```python
@shared_task(queue='default')
def generate_invoice_pdf(invoice_id: str) -> str

@shared_task(queue='high')
def process_invoice_payment(invoice_id: str, payment_intent_id: str) -> None

@shared_task(queue='low')
def send_invoice_email(invoice_id: str) -> None
```

**Validation Checklist**:
- [ ] PDF generation on default queue
- [ ] Payment processing on high queue
- [ ] Email on default queue

---

### Phase 6 Validation

```bash
docker-compose run --rm backend python manage.py makemigrations billing
docker-compose run --rm backend python manage.py migrate
docker-compose run --rm backend python manage.py shell << 'EOF'
from apps.billing.models import Invoice
from apps.organizations.models import Organization
org = Organization.objects.first()
invoice = Invoice.objects.create(
    organization=org,
    subtotal_cents=10000,  # $100
    gst_rate=0.0900,
    due_date=timezone.now() + timedelta(days=30),
    stripe_invoice_id='inv_test123'
)
invoice.refresh_from_db()
print(f'Subtotal: {invoice.subtotal_cents}')
print(f'GST (9%): {invoice.gst_amount_cents}')  # Should be 900
print(f'Total: {invoice.total_amount_cents}')   # Should be 10900
assert invoice.gst_amount_cents == 900, 'GST calculation failed!'
assert invoice.total_amount_cents == 10900, 'Total calculation failed!'
print('GST GeneratedField: OK')
EOF
```

**Success Criteria**:
- [ ] GeneratedField creates database columns
- [ ] $100 subtotal → $9 GST → $109 total
- [ ] Values persist correctly

---

## PHASE 7: Lead Management

**Duration**: Week 6  
**Dependencies**: Phase 3  
**Objective**: Marketing lead capture and tracking

### Files to Create

#### 7.1 `backend/apps/leads/models.py`

**Interface**:
```python
class Lead(models.Model):
    id = UUIDField(primary_key=True)
    name = CharField(max_length=255)
    email = EmailField(db_index=True)
    phone = CharField(max_length=20, blank=True)
    company = CharField(max_length=255)
    job_title = CharField(max_length=100, blank=True)
    source = CharField(choices=['website', 'demo_request', 'contact', 'event', 'referral', 'other'])
    status = CharField(choices=['new', 'contacted', 'qualified', 'converted', 'disqualified'])
    notes = TextField(blank=True)
    utm_source = CharField(max_length=100, blank=True)
    utm_medium = CharField(max_length=100, blank=True)
    utm_campaign = CharField(max_length=100, blank=True)
    utm_term = CharField(max_length=100, blank=True)
    utm_content = CharField(max_length=100, blank=True)
    form_data = JSONField(default=dict)
    assigned_to = ForeignKey(User, null=True, on_delete=SET_NULL)
    next_follow_up = DateTimeField(null=True)
    converted_to_user = ForeignKey(User, null=True, on_delete=SET_NULL, related_name='converted_from_lead')
    converted_at = DateTimeField(null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leads'
        ordering = ['-created_at']
```

**Validation Checklist**:
- [ ] All UTM fields present
- [ ] source and status choices match spec
- [ ] assigned_to nullable
- [ ] converted tracking fields

---

### Phase 7 Validation

```bash
docker-compose run --rm backend python manage.py makemigrations leads
docker-compose run --rm backend python manage.py migrate
```

---

## PHASE 8: PDPA & Privacy Compliance

**Duration**: Week 7  
**Dependencies**: Phase 3  
**Objective**: DSAR with 72-hour SLA and manual approval

### Files to Create

#### 8.1 `backend/apps/privacy/models.py`

**Interface**:
```python
class DSARRequest(models.Model):
    id = UUIDField(primary_key=True)
    user_email = EmailField(db_index=True)
    user = ForeignKey(User, null=True, on_delete=CASCADE)
    request_type = CharField(choices=['export', 'delete', 'access', 'rectification'])
    status = CharField(choices=['pending', 'verifying', 'processing', 'completed', 'failed'])
    verification_token = UUIDField()
    verified_at = DateTimeField(null=True)
    verification_method = CharField(max_length=50, blank=True)
    export_url = URLField(blank=True)
    export_expires_at = DateTimeField(null=True)
    metadata = JSONField(default=dict)
    failure_reason = TextField(blank=True)
    requested_at = DateTimeField(auto_now_add=True)
    processing_started_at = DateTimeField(null=True)
    processed_at = DateTimeField(null=True)
    
    # Manual approval for deletions - CRITICAL
    deletion_approved_by = ForeignKey(User, null=True, on_delete=SET_NULL, related_name='approved_dsar_deletions')
    deletion_approved_at = DateTimeField(null=True)
    
    @property
    def sla_status(self) -> str:
        # Returns 'within_sla', 'approaching_sla', 'breached_sla', 'completed'
    
    @property
    def hours_remaining_in_sla(self) -> float
    
    class Meta:
        db_table = 'dsar_requests'
        constraints = [
            completed_dsar_requires_processed_at,
            deletion_requires_approval  # CRITICAL
        ]
```

**Validation Checklist**:
- [ ] deletion_approved_by field present
- [ ] deletion_requires_approval constraint
- [ ] sla_status property with 72-hour logic
- [ ] hours_remaining_in_sla property

---

#### 8.2 `backend/apps/privacy/tasks.py`

**Interface**:
```python
@shared_task(queue='low')
def process_dsar_export(dsar_id: str) -> str:
    # Generate data export
    # Upload to S3
    # Set export_expires_at (7 days)    # Return export_url

@shared_task(queue='default')
def send_dsar_verification_email(dsar_id: str) -> None

@shared_task(queue='default')
def send_dsar_complete_email(dsar_id: str) -> None

@shared_task
def enforce_pdpa_retention() -> dict:
    # Called by Celery beat
    # Clean up expired exports
    # Remove old anonymized data
```

**Validation Checklist**:
- [ ] Export on low priority queue
- [ ] 72-hour SLA tracked
- [ ] Export expires after 7 days
- [ ] Retention task for Celery beat

---

### Phase 8 Validation

```bash
docker-compose run --rm backend python manage.py makemigrations privacy
docker-compose run --rm backend python manage.py migrate
docker-compose run --rm backend python manage.py shell << 'EOF'
from apps.privacy.models import DSARRequest
from django.utils import timezone
dsar = DSARRequest(
    user_email='test@test.com',
    request_type='export',
    status='pending'
)
dsar.save()
print(f'SLA Status: {dsar.sla_status}')  # Should be 'within_sla'
print(f'Hours remaining: {dsar.hours_remaining_in_sla}')  # Should be ~72
print('DSAR model: OK')
EOF
```

---

## PHASE 9: Webhooks & Integration

**Duration**: Week 8-9  
**Dependencies**: Phase 6  
**Objective**: Stripe webhook handling with idempotency

### Files to Create

#### 9.1 `backend/apps/webhooks/handlers/stripe.py`

**Interface**:
```python
class StripeWebhookHandler:
    @staticmethod
    def handle_event(event: WebhookEvent) -> bool
    
    @staticmethod
    def handle_invoice_paid(event_data: dict) -> None
    
    @staticmethod
    def handle_invoice_payment_failed(event_data: dict) -> None
    
    @staticmethod
    def handle_subscription_updated(event_data: dict) -> None
    
    @staticmethod
    def handle_subscription_deleted(event_data: dict) -> None
```

**Validation Checklist**:
- [ ] Signature verification
- [ ] WebhookEvent deduplication by event_id
- [ ] Retry logic with exponential backoff
- [ ] Event logging

---

#### 9.2 `backend/apps/webhooks/views.py`

**Interface**:
```python
class StripeWebhookView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Verify Stripe signature
        # Check for duplicate event_id
        # Create WebhookEvent record
        # Enqueue processing task
        # Return 200 immediately
```

**Validation Checklist**:
- [ ] Returns 200 immediately (async processing)
- [ ] Stripe signature verified
- [ ] WebhookEvent created for tracking
- [ ] Duplicate events rejected (200)

---

#### 9.3 `backend/apps/webhooks/tasks.py`

**Interface**:
```python
@shared_task(queue='high', bind=True, max_retries=3)
def process_stripe_webhook(self, webhook_event_id: str) -> bool:
    # Load WebhookEvent
    # Call appropriate handler
    # Mark processed
    # Handle errors with retry

@shared_task(queue='high')
def process_stripe_subscription(subscription_id: str, payment_method_id: str, idempotency_key: str) -> None
```

**Validation Checklist**:
- [ ] High priority queue
- [ ] max_retries=3
- [ ] bind=True for self access
- [ ] Retry on failure

---

### Phase 9 Validation

```bash
docker-compose run --rm backend python manage.py test apps.webhooks
```

---

## PHASE 10: Frontend Foundation

**Duration**: Week 9-10  
**Dependencies**: None (parallel)  
**Objective**: Next.js 14 setup with Elementra design system

### Files to Create

#### 10.1 `frontend/package.json`

**Validation Checklist**:
- [ ] next: ^14.0.0
- [ ] react: ^18.0.0
- [ ] typescript: ^5.0.0
- [ ] tailwindcss: ^3.4.0
- [ ] axios
- [ ] @tanstack/react-query

---

#### 10.2 `frontend/tailwind.config.js`

**Interface**:
```javascript
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        singapore: {
          red: '#eb582d',
          blue: '#1e3a8a',
        },
        primary: { 50-900 scale },
        secondary: { 50-900 scale },
        glass: { light, DEFAULT, dark },
        dark: { 50-900 scale },
      },
    },
  },
}
```

**Validation Checklist**:
- [ ] singapore.red = '#eb582d'
- [ ] singapore.blue = '#1e3a8a'
- [ ] darkMode = 'class'
- [ ] All color scales defined

---

#### 10.3 `frontend/src/app/layout.tsx`

**Validation Checklist**:
- [ ] Root layout with providers
- [ ] QueryClientProvider
- [ ] ThemeProvider
- [ ] SEO meta tags

---

#### 10.4 `frontend/src/lib/api/client.ts`

**Interface**:
```typescript
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Add auth interceptor
// Add error interceptor
// Add idempotency key generator for mutations
```

**Validation Checklist**:
- [ ] Base URL from environment
- [ ] Auth token in headers
- [ ] Idempotency key support

---

#### 10.5 `frontend/src/types/models.ts`

**Interface**:
```typescript
interface User {
  id: string;
  email: string;
  name: string;
  company?: string;
  timezone: string;
  is_verified: boolean;
}

interface Organization {
  id: string;
  name: string;
  slug: string;
  uen: string;
  is_gst_registered: boolean;
  gst_reg_no?: string;
}

interface Invoice {
  id: string;
  subtotal_cents: number;
  gst_rate: number;
  gst_amount_cents: number;
  total_amount_cents: number;
  iras_transaction_code: 'SR' | 'ZR' | 'OS' | 'TX';
  currency: 'SGD';
  status: 'draft' | 'open' | 'paid' | 'void' | 'uncollectible';
}
```

**Validation Checklist**:
- [ ] All models typed
- [ ] GST fields on Invoice
- [ ] UEN on Organization
- [ ] Matches backend exactly

---

### Phase 10 Validation

```bash
cd frontend
npm install
npm run build
npm run lint
```

---

## PHASE 11: Frontend Application

**Duration**: Week 10-11  
**Dependencies**: Phase 10  
**Objective**: All pages and components

### Files to Create

#### 11.1 Marketing Pages (SSG)
- `src/app/page.tsx` - Homepage
- `src/app/(marketing)/pricing/page.tsx`
- `src/app/(marketing)/about/page.tsx`
- `src/app/(marketing)/contact/page.tsx`

**Validation Checklist**:
- [ ] SSG with generateStaticParams where needed
- [ ] SEO metadata
- [ ] Singapore color palette used
- [ ] Mobile responsive

---

#### 11.2 Auth Pages
- `src/app/(auth)/login/page.tsx`
- `src/app/(auth)/signup/page.tsx`
- `src/app/(auth)/verify/page.tsx`

**Validation Checklist**:
- [ ] Form validation
- [ ] Error handling
- [ ] Loading states

---

#### 11.3 Application Pages (SSR)
- `src/app/(app)/dashboard/page.tsx`
- `src/app/(app)/leads/page.tsx`
- `src/app/(app)/subscriptions/page.tsx`
- `src/app/(app)/invoices/page.tsx`
- `src/app/(app)/settings/page.tsx`

**Validation Checklist**:
- [ ] Auth required
- [ ] SSR with getServerSideProps equivalent
- [ ] Loading/error states
- [ ] GST amounts displayed correctly

---

#### 11.4 Components
- `src/components/ui/` - Button, Input, Card, Modal, etc.
- `src/components/marketing/` - Hero, Features, PricingCard
- `src/components/forms/` - LoginForm, SignupForm, LeadForm
- `src/components/domain/` - InvoiceRow, SubscriptionCard

**Validation Checklist for PricingCard**:
- [ ] Uses `singapore-red` for featured plan
- [ ] Shows GST note "All prices exclude 9% GST"
- [ ] Annual savings percentage

---

### Phase 11 Validation

```bash
npm run build
npm run test
npx cypress run
```

---

## PHASE 12: Testing & Production

**Duration**: Week 12-13  
**Dependencies**: All previous  
**Objective**: Tests, security, deployment

### Files to Create

#### 12.1 `backend/tests/test_merge_validation.py`

**Validation Checklist**:
- [ ] test_idempotency_record_exists
- [ ] test_webhook_event_exists
- [ ] test_gst_generated_field
- [ ] test_uen_validation
- [ ] test_singapore_timezone

---

#### 12.2 `backend/tests/test_gst_compliance.py`

**Validation Checklist**:
- [ ] test_gst_calculation_accuracy
- [ ] test_iras_transaction_codes
- [ ] test_gst_rounding
- [ ] test_zero_rate_gst

---

#### 12.3 `docker-compose.prod.yml`

**Validation Checklist**:
- [ ] Gunicorn with multiple workers
- [ ] Nginx with SSL
- [ ] Health checks on all services
- [ ] Resource limits defined
- [ ] Secrets from environment

---

#### 12.4 `.github/workflows/ci.yml`

**Validation Checklist**:
- [ ] Runs on push to main/develop
- [ ] Python tests with pytest
- [ ] Frontend tests with jest
- [ ] Linting (ruff, eslint)
- [ ] Type checking (mypy, tsc)

---

### Phase 12 Validation

```bash
# Full test suite
docker-compose run --rm backend pytest --cov=apps
cd frontend && npm run test:coverage

# Production build
docker-compose -f docker-compose.prod.yml config
docker-compose -f docker-compose.prod.yml build

# Security scan
pip install safety && safety check
npm audit
```

**Final Success Criteria**:
- [ ] All tests pass
- [ ] No security vulnerabilities (high/critical)
- [ ] GST calculations verified
- [ ] DSAR 72-hour SLA tracked
- [ ] Production builds successfully
- [ ] Health checks respond

---

## Appendix: File Count Summary

| Phase | Backend Files | Frontend Files | Config Files |
|-------|---------------|----------------|--------------|
| 1 | 9 | 0 | 3 |
| 2 | 9 | 0 | 0 |
| 3 | 9 | 0 | 0 |
| 4 | 5 | 0 | 0 |
| 5 | 4 | 0 | 0 |
| 6 | 4 | 0 | 0 |
| 7 | 4 | 0 | 0 |
| 8 | 4 | 0 | 0 |
| 9 | 4 | 0 | 0 |
| 10 | 0 | 8 | 3 |
| 11 | 0 | 25 | 0 |
| 12 | 4 | 2 | 3 |
| **Total** | **56** | **35** | **9** |

**Grand Total: 100 files**

> ✅ **Validated against**:
> - Project_Architecture_Document.md (PAD)
> - NexusCore-v4.0-Merged-PRD.md
> - comprehensive_analysis_validation.md

---

*Document generated: 2025-12-23 | NexusCore v4.0 Master Execution Plan*
