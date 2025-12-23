# NexusCore v4.0 — AI Coding Agent Briefing Handbook

> **Single-Source-of-Truth for Implementation**  
> Version: 1.0.0 | Date: 2025-12-23 | Status: Ready for Implementation

---

## Document Purpose

This handbook provides **complete context** for any AI coding agent or developer to implement NexusCore v4.0. It synthesizes four source documents into actionable knowledge:

| Source Document | Purpose |
|-----------------|---------|
| `NexusCore-v4.0-Merged-PRD.md` | Complete merged specification |
| `Project_Architecture_Document.md` | C4 diagrams and implementation blueprints |
| `PRD-qd-3-appendix.md` | Strict Merge Strategy rationale |
| `PAD-Validation-Analysis.md` | Validation and approval status |

---

## 1. Project Identity

### 1.1 What is NexusCore?
**NexusCore v4.0** is a Singapore-first B2B SaaS platform designed for production deployment. It is the strategic merger of:
- **PRD-d-3** (Infrastructure Layer): Idempotency, Webhooks, Event Logging, Monitoring
- **PRD-q-3** (Domain Layer): GST compliance, UEN validation, PDPA automation

### 1.2 Why the Merge?
> **CRITICAL**: A pure implementation of PRD-q-3 would **fail at runtime** because it silently depends on models defined only in PRD-d-3.

Example failure without merge:
```python
# PRD-q-3 SubscriptionViewSet.create references:
existing = IdempotencyRecord.objects.filter(...)  # NameError!
# IdempotencyRecord is ONLY defined in PRD-d-3
```

### 1.3 Primary Stack
| Layer | Technology | Version |
|-------|------------|---------|
| Backend | Django | 6.0 |
| Frontend | Next.js | 14 |
| Database | PostgreSQL | 16+ (REQUIRED) |
| Cache/Broker | Redis | 7.4 |
| Task Queue | Celery | 5.x |
| Python | Python | 3.12+ |

---

## 2. Singapore Regulatory Compliance

### 2.1 GST (Goods & Services Tax)
| Requirement | Implementation |
|-------------|----------------|
| Rate | 9% (0.0900) |
| Calculation | **Database-level** via `GeneratedField` |
| Audit Trail | Immutable at storage layer |
| IRAS Codes | SR (Standard), ZR (Zero), OS (Out of Scope), TX (Taxable) |

```python
# CRITICAL: GST calculated at database level, NOT application level
gst_amount_cents = models.GeneratedField(
    expression=models.Func(
        models.F('subtotal_cents') * models.F('gst_rate'),
        function='ROUND',
        output_field=models.BigIntegerField()
    ),
    output_field=models.BigIntegerField(),
    db_persist=True  # Persisted for query performance & audit
)
```

**Why database-level?**
1. GST calculation cannot drift between application instances
2. Floating-point precision errors prevented by `ROUND()`
3. Audit trail is immutable

### 2.2 UEN (Unique Entity Number)
All organizations must have a valid Singapore UEN registered with ACRA.

```python
# Valid UEN formats (regex):
# Format 1: 8 digits + 1 letter (e.g., 12345678A)
# Format 2: 9 digits + 1 letter (e.g., 123456789B)
# Format 3: T/S/R/Q + 2 digits + 4 alphanumeric + 3 digits + 1 letter
uen = models.CharField(
    max_length=15,
    unique=True,
    validators=[
        RegexValidator(
            regex=r'^[0-9]{8}[A-Z]$|^[0-9]{9}[A-Z]$|^[TSRQ][0-9]{2}[A-Z0-9]{4}[0-9]{3}[A-Z]$',
            message="Enter a valid Singapore UEN."
        )
    ]
)
```

### 2.3 PDPA (Personal Data Protection Act)
| Requirement | Implementation |
|-------------|----------------|
| DSAR SLA | 72 hours |
| Deletion Approval | **Manual approval required** via `deletion_approved_by` |
| Data Residency | Singapore region (`ap-southeast-1`) |
| Retention | Automated via Celery beat task |

---

## 3. Core Data Models

### 3.1 Model Hierarchy
```
User (auth)
├── OrganizationMembership
│   └── Organization (Singapore compliance: UEN, GST)
│       ├── Subscription
│       │   └── Invoice (GST GeneratedFields)
│       ├── Lead
│       └── DSARRequest (PDPA compliance)
├── Event (audit logging)
├── IdempotencyRecord (duplicate prevention)
└── WebhookEvent (external webhooks)
```

### 3.2 Critical Models from PRD-d-3 (Infrastructure)

> ⚠️ **MUST IMPLEMENT FIRST** — Domain logic depends on these

| Model | Purpose | Dependencies |
|-------|---------|--------------|
| `IdempotencyRecord` | Prevent duplicate operations | Used by SubscriptionViewSet |
| `WebhookEvent` | Track external webhooks | Used by Stripe handler |
| `Event` | Audit logging | Used by all mutations |

### 3.3 Critical Models from PRD-q-3 (Domain)

| Model | Purpose | Singapore Feature |
|-------|---------|-------------------|
| `Organization` | Company entity | UEN, GST registration |
| `Invoice` | Billing | GST `GeneratedField` |
| `DSARRequest` | Privacy requests | 72-hour SLA, manual approval |

---

## 4. API Architecture

### 4.1 Endpoint Structure
```
/api/v1/
├── auth/                  # Authentication
├── users/                 # User management
├── organizations/         # Organization management
├── subscriptions/         # Subscription management (requires Idempotency-Key)
├── invoices/              # GST-compliant invoices
├── leads/                 # Lead management
├── dsar/                  # PDPA DSAR endpoints
├── events/                # Analytics events
└── webhooks/              # External webhook handlers
    └── stripe/            # Stripe webhook endpoint
```

### 4.2 Idempotency Pattern
All payment-related operations **MUST** include an `Idempotency-Key` header:

```python
# Request
POST /api/v1/subscriptions/
Headers:
  Idempotency-Key: unique-client-generated-key
  Authorization: Bearer <token>

# Response (if duplicate)
HTTP 202 Accepted
{"status": "processing", "idempotency_key": "..."}

# Response (if completed previously)
HTTP 200 OK (cached response)
```

### 4.3 Django 6.0 Async Support
The codebase uses Django 6.0's native async ORM methods:
- `Model.objects.aget()` — async get
- `Model.objects.acreate()` — async create
- `instance.asave()` — async save

---

## 5. Frontend Architecture

### 5.1 Next.js 14 App Router Structure
```
src/app/
├── (marketing)/           # SSG - Static generation
│   ├── page.tsx           # Homepage
│   ├── pricing/           # Pricing page
│   └── about/             # About page
├── (auth)/                # Auth flows
│   ├── login/
│   ├── signup/
│   └── verify/
└── (app)/                 # SSR - Server-side rendering
    ├── dashboard/
    ├── leads/
    ├── subscriptions/
    ├── invoices/
    └── settings/
```

### 5.2 Design System: Elementra

**Singapore Color Palette** (MUST be in `tailwind.config.js`):
```javascript
colors: {
  singapore: {
    red: '#eb582d',   // Primary actions
    blue: '#1e3a8a',  // Trust blue for backgrounds
  },
  // ... other colors from PRD-d-3
}
```

> ⚠️ **Silent Failure Risk**: PRD-q-3 components use `border-singapore-red` but PRD-d-3's Tailwind config doesn't define it. Verify this is merged.

### 5.3 Performance Targets
| Metric | Target | Validation |
|--------|--------|------------|
| Mobile LCP | ≤2.5s (launch), ≤2.0s (60 days) | Lighthouse |
| Bundle Size | Critical CSS optimized | Webpack analyzer |
| Accessibility | WCAG AA | axe-core |

---

## 6. Infrastructure

### 6.1 Docker Services
| Service | Image | Purpose |
|---------|-------|---------|
| `nginx` | nginx:1.25 | Reverse proxy |
| `backend` | Django 6.0 + Gunicorn | API server |
| `frontend` | Next.js 14 | Web application |
| `celery` | Celery 5.4 | Task workers |
| `postgres` | postgres:16 | Primary database |
| `redis` | redis:7.4 | Cache + Celery broker |

### 6.2 Critical Environment Variables
```bash
# DATABASE (PostgreSQL 16 REQUIRED for GeneratedField)
DB_NAME=nexuscore
DB_USER=nexuscore_user
DB_HOST=postgres
DB_PORT=5432

# AWS (Singapore region REQUIRED for PDPA)
AWS_S3_REGION_NAME=ap-southeast-1

# STRIPE
STRIPE_SECRET_KEY=sk_...
STRIPE_WEBHOOK_SECRET=whsec_...

# CELERY
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_TIMEZONE=Asia/Singapore

# PDPA
PDPA_DSAR_SLA_HOURS=72
```

### 6.3 Database Requirements
- **PostgreSQL 16+** is **REQUIRED** for `GeneratedField` support
- `CONN_HEALTH_CHECKS = True` for connection pooling
- Statement timeout: 5000ms

---

## 7. Implementation Order

### 7.1 Non-Negotiable Sequence
The Strict Merge Strategy dictates this order:

```
Phase 1: Foundation (Weeks 1-4)
├── IdempotencyRecord model      ← CRITICAL: Must exist first
├── WebhookEvent model           ← CRITICAL: Must exist first
├── Event model                  ← CRITICAL: Must exist first
├── User model
├── Organization model (with UEN)
├── OrganizationMembership model
└── Docker environment setup

Phase 2: Compliance Engine (Weeks 5-7)
├── Invoice model (with GST GeneratedField)
├── UEN validation in Organization
├── IRAS transaction codes
├── PDPA retention policies
└── DSARRequest workflows

Phase 3: Payments & Integration (Weeks 8-9)
├── Stripe webhook handlers
├── Subscription model
├── Invoice generation with GST
└── PDF generation with IRAS formatting

Phase 4: Production Hardening (Weeks 10-13)
├── DSAR workflow validation
├── 72-hour SLA automation
├── Security audit
├── Performance optimization
└── Blue-green deployment
```

### 7.2 Risk Mitigation

| Risk | Cause | Mitigation |
|------|-------|------------|
| **Runtime NameError** | Missing `IdempotencyRecord` | Implement infrastructure models FIRST |
| **CSS Missing** | `singapore-red` not in Tailwind | Verify merged Tailwind config |
| **GeneratedField Fails** | PostgreSQL < 16 | Pin `postgres:16-alpine` in Docker |
| **Task Pattern Mismatch** | `.enqueue()` vs `.delay()` | Standardize on `.delay()` for Celery |

---

## 8. Testing Strategy

### 8.1 Merge Validation Tests
Before any domain logic, run these tests:

```python
@pytest.mark.django_db
class TestMergeValidation:
    def test_idempotency_record_exists(self):
        """PRD-d-3 dependency available"""
        from apps.core.models import IdempotencyRecord
        record = IdempotencyRecord.objects.create(
            key='test-key',
            request_path='/api/v1/subscriptions/',
            request_method='POST',
            request_hash='abc123',
            status='processing',
            expires_at=timezone.now() + timedelta(hours=24)
        )
        assert record.id is not None

    def test_gst_generated_field(self):
        """PRD-q-3 feature works"""
        # Create invoice with subtotal
        invoice = Invoice.objects.create(
            subtotal_cents=10000,  # $100.00
            gst_rate=0.0900,
            ...
        )
        invoice.refresh_from_db()
        assert invoice.gst_amount_cents == 900     # 9%
        assert invoice.total_amount_cents == 10900  # $109.00
```

### 8.2 Coverage Targets
| Category | Target | Tools |
|----------|--------|-------|
| Critical Paths | ≥70% | pytest, coverage |
| API Endpoints | 100% | pytest-drf |
| E2E Flows | Key flows | Cypress |
| Performance | P95 < 500ms | k6 |

---

## 9. Quick Reference

### 9.1 Key Files
| Purpose | Path |
|---------|------|
| Django Settings | `backend/config/settings/` |
| Core Models | `backend/apps/core/models.py` |
| Celery Config | `backend/config/celery.py` |
| Tailwind Config | `frontend/tailwind.config.js` |
| Docker Compose | `docker-compose.yml` |
| Environment | `.env.example` |

### 9.2 Celery Task Queues
| Queue | Priority | Use For |
|-------|----------|---------|
| `high` | P0 | Webhooks, payment processing |
| `default` | P1 | Emails, notifications |
| `low` | P2 | Reports, cleanup, DSAR exports |

### 9.3 Common Commands
```bash
# Development
docker-compose up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py test

# Production
docker-compose -f docker-compose.prod.yml up -d

# Celery
celery -A config worker -Q high,default,low -l INFO
celery -A config beat -l INFO
```

---

## 10. Success Criteria

### 10.1 Business Metrics
| Metric | Target |
|--------|--------|
| Trial → Paid Conversion | ≥15% within 30 days |
| CTA Conversion | ≥5% on pricing pages |
| Payment Webhook Success | ≥99.9% |
| DSAR SLA Compliance | 100% within 72 hours |
| GST Accuracy | 100% IRAS compliant |

### 10.2 Technical Metrics
| Metric | Target |
|--------|--------|
| Mobile LCP | ≤2.5s |
| API P95 Latency | <500ms |
| Test Coverage | ≥70% critical paths |
| Uptime | ≥99.9% |

---

## Appendix A: Model Field Reference

### A.1 Organization (Singapore)
| Field | Type | Constraint |
|-------|------|------------|
| `uen` | VARCHAR(15) | ACRA regex, UNIQUE |
| `is_gst_registered` | BOOLEAN | Default FALSE |
| `gst_reg_no` | VARCHAR(20) | Regex: `^M[0-9]{8}[A-Z]$` |
| `billing_email` | EMAIL | Required |
| `timezone` | VARCHAR(50) | Default: Asia/Singapore |

### A.2 Invoice (GST)
| Field | Type | Notes |
|-------|------|-------|
| `subtotal_cents` | BIGINT | Net before tax |
| `gst_rate` | DECIMAL(5,4) | Default: 0.0900 |
| `gst_amount_cents` | BIGINT | **GENERATED** |
| `total_amount_cents` | BIGINT | **GENERATED** |
| `iras_transaction_code` | VARCHAR(10) | SR/ZR/OS/TX |
| `currency` | VARCHAR(3) | Default: SGD |

### A.3 IdempotencyRecord
| Field | Type | Notes |
|-------|------|-------|
| `key` | VARCHAR(255) | UNIQUE, indexed |
| `request_path` | VARCHAR(255) | e.g., `/api/v1/subscriptions/` |
| `request_method` | VARCHAR(10) | POST/PUT/PATCH |
| `request_hash` | VARCHAR(64) | SHA256 of body |
| `status` | VARCHAR(20) | processing/completed/failed |
| `expires_at` | TIMESTAMP | 24 hours default |

---

## Appendix B: Compliance Checklist

### B.1 Before Go-Live
- [ ] GST `GeneratedField` tested with production data
- [ ] UEN validation rejects invalid formats
- [ ] DSAR export completes within 72 hours
- [ ] DSAR deletion requires manual approval
- [ ] All data in `ap-southeast-1` region
- [ ] Invoice PDF includes IRAS transaction code
- [ ] Idempotency prevents duplicate payments

### B.2 Ongoing
- [ ] DSAR SLA monitored (72-hour threshold)
- [ ] GST rate configurable for future changes
- [ ] Audit events logged for all mutations
- [ ] Webhook failures trigger alerts

---

*Document generated: 2025-12-23 | NexusCore v4.0 Strict Merge Strategy*
