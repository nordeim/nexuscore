# 🚀 NexusCore — Singapore Enterprise SaaS Platform

<div align="center">

![NexusCore](https://img.shields.io/badge/NexusCore-Singapore_SaaS_Platform-eb582d?style=for-the-badge&logo=rocket&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.12+-blue?style=flat-square&logo=python)](https://www.python.org)
[![Django](https://img.shields.io/badge/Django-6.0-green?style=flat-square&logo=django)](https://www.djangoproject.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.2-black?style=flat-square&logo=next.js)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue?style=flat-square&logo=postgresql)](https://www.postgresql.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)

**Enterprise-grade SaaS platform built for Singapore businesses**

🇸🇬 GST Compliant • 🔒 PDPA Ready • ✅ UEN Validated

[**Live Demo**](https://demo.nexuscore.sg) · [**Documentation**](https://docs.nexuscore.sg) · [**API Reference**](https://api.nexuscore.sg/docs)

</div>

---

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| **Backend Apps** | 9 Django apps |
| **Database Tables** | 11 models |
| **Frontend Routes** | 13 pages |
| **Files Created** | 110+ |
| **Development Phases** | 11/12 complete |

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Module Interactions](#-module-interactions)
- [Singapore Compliance](#-singapore-compliance)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [API Documentation](#-api-documentation)
- [User Journey](#-user-journey)
- [Development Status](#-development-status)
- [Contributing](#-contributing)

---

## 🌐 Overview

NexusCore v4.0 is a production-ready B2B SaaS platform designed specifically for Singapore businesses. Unlike generic SaaS platforms, NexusCore implements **compliance at the database level**:

| Feature | Implementation |
|---------|----------------|
| **GST Calculation** | PostgreSQL `GeneratedField` — zero floating-point errors |
| **PDPA Automation** | 72-hour DSAR SLA with manual deletion approval |
| **UEN Validation** | ACRA-format regex validation for all organizations |

### Why NexusCore?

- **🇸🇬 Singapore-First**: Built for local regulatory requirements from day one
- **📊 Database-Level Compliance**: GST calculated in PostgreSQL, not application code
- **🔒 PDPA Automation**: 72-hour SLA tracking with mandatory approval workflows
- **⚡ Modern Stack**: Django 6.0 (latest) + Next.js 14 App Router
- **🔄 Event-Driven**: Celery workers for async operations, Stripe webhooks

---

## 🏗️ Architecture

### System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Next.js 14 Frontend]
        MOBILE[Mobile PWA]
    end
    
    subgraph "API Layer"
        API[Django 6.0 REST API]
        WS[WebSocket Server]
    end
    
    subgraph "Background Services"
        CELERY[Celery Workers]
        BEAT[Celery Beat Scheduler]
    end
    
    subgraph "Data Layer"
        PG[(PostgreSQL 16)]
        REDIS[(Redis 7.4)]
    end
    
    subgraph "External Services"
        STRIPE[Stripe Payments]
        EMAIL[SendGrid Email]
    end
    
    WEB --> API
    MOBILE --> API
    API --> PG
    API --> REDIS
    API --> CELERY
    CELERY --> PG
    CELERY --> STRIPE
    CELERY --> EMAIL
    BEAT --> CELERY
    
    style WEB fill:#0070f3
    style API fill:#092e20
    style PG fill:#336791
    style REDIS fill:#dc382d
    style STRIPE fill:#635bff
```

### Data Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Auth
    participant Business
    participant DB
    participant Cache
    participant Worker
    
    Client->>API: POST /api/v1/subscriptions/
    API->>Auth: Validate JWT Token
    Auth->>Cache: Check Session
    Cache-->>Auth: Session Valid
    Auth-->>API: Authorized
    
    API->>Business: Create Subscription
    Business->>DB: Check Idempotency
    
    alt Duplicate Request
        DB-->>Business: Existing Record
        Business-->>API: Return Cached Response
    else New Request
        Business->>DB: Create Subscription
        Business->>Worker: Queue Invoice Generation
        Worker->>DB: Create Invoice (GST GeneratedField)
        Worker->>DB: Log Event
    end
    
    Business-->>API: Response
    API-->>Client: 201 Created
```

---

## 🔗 Module Interactions

### Backend App Dependencies

```mermaid
graph LR
    subgraph "Core Layer"
        CORE[core]
        EVENTS[events]
    end
    
    subgraph "Auth Layer"
        USERS[users]
    end
    
    subgraph "Business Layer"
        ORGS[organizations]
        SUBS[subscriptions]
        BILLING[billing]
        LEADS[leads]
    end
    
    subgraph "Compliance Layer"
        PRIVACY[privacy]
        WEBHOOKS[webhooks]
    end
    
    USERS --> CORE
    ORGS --> USERS
    ORGS --> EVENTS
    SUBS --> ORGS
    BILLING --> SUBS
    BILLING --> EVENTS
    LEADS --> ORGS
    PRIVACY --> USERS
    PRIVACY --> EVENTS
    WEBHOOKS --> SUBS
    WEBHOOKS --> BILLING
    WEBHOOKS --> EVENTS
    
    style CORE fill:#4a5568
    style BILLING fill:#eb582d
    style PRIVACY fill:#1e3a8a
```

### Model Relationships

```mermaid
erDiagram
    User ||--o{ OrganizationMembership : has
    Organization ||--o{ OrganizationMembership : has
    Organization ||--o{ Subscription : has
    Organization ||--o{ Lead : has
    Subscription ||--o{ Invoice : generates
    User ||--o{ DSARRequest : submits
    User ||--o{ Event : triggers
    
    Organization {
        uuid id PK
        string uen UK
        string gst_reg_no
        boolean is_gst_registered
    }
    
    Invoice {
        uuid id PK
        bigint subtotal_cents
        decimal gst_rate
        bigint gst_amount_cents "GENERATED"
        bigint total_amount_cents "GENERATED"
        string iras_transaction_code
    }
    
    DSARRequest {
        uuid id PK
        string request_type
        string status
        timestamp created_at
        int sla_hours "72"
    }
```

---

## 🇸🇬 Singapore Compliance

### GST (Goods & Services Tax)

| Requirement | Implementation |
|-------------|----------------|
| **Rate** | 9% (0.0900) |
| **Calculation** | PostgreSQL `GeneratedField` |
| **IRAS Codes** | SR, ZR, OS, TX |
| **Currency** | SGD (default) |
| **Audit Trail** | Immutable at database level |

```python
# Database-level GST calculation (no floating-point errors)
gst_amount_cents = GeneratedField(
    expression=Round(F('subtotal_cents') * F('gst_rate')),
    db_persist=True
)
```

### PDPA (Personal Data Protection Act)

| Requirement | Implementation |
|-------------|----------------|
| **DSAR SLA** | 72 hours |
| **Deletion** | Manual approval required |
| **Data Export** | Automated via Celery |
| **Residency** | Singapore region (ap-southeast-1) |

### UEN (Unique Entity Number)

```python
# ACRA-compliant UEN validation
uen = models.CharField(
    max_length=15,
    validators=[RegexValidator(
        regex=r'^[0-9]{8}[A-Z]$|^[0-9]{9}[A-Z]$|^[TSRQ][0-9]{2}[A-Z0-9]{4}[0-9]{3}[A-Z]$'
    )]
)
```

---

## 💻 Tech Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.12+ | Runtime |
| **Django** | 6.0 | Web framework (GeneratedField support) |
| **DRF** | 3.15+ | REST API |
| **Celery** | 5.4+ | Async task queue |
| **PostgreSQL** | 16+ | Database (required) |
| **Redis** | 7.4+ | Cache & message broker |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Next.js** | 14.2 | React framework (App Router) |
| **React** | 18 | UI library |
| **TypeScript** | 5 | Type safety |
| **Tailwind CSS** | 3.4 | Styling |
| **React Query** | 5 | Server state |
| **Axios** | 1.13 | HTTP client |

---

## 📁 Project Structure

### Complete File Hierarchy

```
nexuscore/
├── 📦 backend/                          # Django 6.0 backend
│   ├── 📁 apps/                         # Django applications
│   │   ├── 🔐 users/                    # User authentication
│   │   │   ├── models.py               # CustomUser model
│   │   │   ├── views.py                # Auth ViewSets
│   │   │   ├── serializers.py          # User serializers
│   │   │   ├── permissions.py          # Custom permissions
│   │   │   └── urls.py                 # Auth routes
│   │   │
│   │   ├── 🏢 organizations/            # Organization management
│   │   │   ├── models.py               # Organization + Membership
│   │   │   ├── views.py                # Org CRUD ViewSet
│   │   │   ├── serializers.py          # UEN validation
│   │   │   └── admin.py                # Admin interface
│   │   │
│   │   ├── 📋 subscriptions/            # Subscription management
│   │   │   ├── models.py               # Plan + Subscription
│   │   │   ├── views.py                # Idempotent creation
│   │   │   ├── services.py             # Stripe integration
│   │   │   └── tasks.py                # Async operations
│   │   │
│   │   ├── 💰 billing/                  # Invoice & GST
│   │   │   ├── models/
│   │   │   │   └── invoice.py          # GST GeneratedFields
│   │   │   ├── views.py                # Invoice ViewSet
│   │   │   ├── services.py             # PDF generation
│   │   │   └── admin.py                # GST badges
│   │   │
│   │   ├── 👥 leads/                    # Lead management
│   │   │   ├── models.py               # Lead + UTM tracking
│   │   │   ├── views.py                # Lead ViewSet
│   │   │   └── tasks.py                # Lead scoring
│   │   │
│   │   ├── 🔒 privacy/                  # PDPA compliance
│   │   │   ├── models.py               # DSARRequest (72hr SLA)
│   │   │   ├── views.py                # DSAR endpoints
│   │   │   ├── tasks.py                # Export/deletion
│   │   │   └── admin.py                # SLA badges
│   │   │
│   │   ├── 🔔 webhooks/                 # External webhooks
│   │   │   ├── models.py               # WebhookEvent
│   │   │   ├── handlers/
│   │   │   │   └── stripe.py           # Stripe handler
│   │   │   ├── views.py                # Webhook receiver
│   │   │   └── tasks.py                # Async processing
│   │   │
│   │   ├── 📊 events/                   # Audit logging
│   │   │   ├── models.py               # Event + IdempotencyRecord
│   │   │   └── admin.py                # Event browser
│   │   │
│   │   └── 🧩 core/                     # Shared utilities
│   │       └── base_model.py           # UUID mixin
│   │
│   ├── ⚙️ config/                       # Django configuration
│   │   ├── settings/
│   │   │   ├── base.py                 # Core settings
│   │   │   ├── development.py          # Dev settings
│   │   │   └── production.py           # Prod settings
│   │   ├── urls.py                     # URL routing
│   │   ├── celery.py                   # Celery config
│   │   ├── wsgi.py                     # WSGI entry
│   │   └── asgi.py                     # ASGI entry
│   │
│   ├── pyproject.toml                   # Dependencies (uv)
│   └── manage.py                        # Django CLI
│
├── 🎨 frontend/                         # Next.js 14 frontend
│   ├── 📁 src/
│   │   ├── 📄 app/                      # App Router pages
│   │   │   ├── page.tsx                # Homepage (premium design)
│   │   │   ├── layout.tsx              # Root layout + providers
│   │   │   │
│   │   │   ├── (marketing)/            # SSG marketing pages
│   │   │   │   ├── layout.tsx          # Header + footer
│   │   │   │   └── pricing/page.tsx    # Pricing + GST note
│   │   │   │
│   │   │   ├── (auth)/                 # Authentication
│   │   │   │   ├── layout.tsx          # Centered auth layout
│   │   │   │   ├── login/page.tsx      # Login form
│   │   │   │   ├── signup/page.tsx     # Signup form
│   │   │   │   └── verify/page.tsx     # Email verification
│   │   │   │
│   │   │   └── (app)/                  # Authenticated app
│   │   │       ├── layout.tsx          # Sidebar layout
│   │   │       ├── dashboard/page.tsx  # Dashboard stats
│   │   │       ├── leads/page.tsx      # Lead table
│   │   │       ├── invoices/page.tsx   # Invoice table + GST
│   │   │       └── settings/page.tsx   # Settings + PDPA
│   │   │
│   │   ├── 🧩 components/
│   │   │   ├── ui/                     # Button, Input, Card
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   └── Card.tsx
│   │   │   └── marketing/              # Hero, PricingCard
│   │   │       ├── Hero.tsx
│   │   │       └── PricingCard.tsx
│   │   │
│   │   ├── 📚 lib/
│   │   │   ├── api/
│   │   │   │   └── client.ts           # Axios + interceptors
│   │   │   └── providers.tsx           # React Query + Theme
│   │   │
│   │   └── 📝 types/
│   │       └── models.ts               # TypeScript interfaces
│   │
│   ├── tailwind.config.ts              # Singapore colors
│   ├── package.json                    # Dependencies
│   └── tsconfig.json                   # TypeScript config
│
└── 📚 docs/                             # Documentation
    ├── NexusCore-v4.0-Merged-PRD.md    # Product requirements
    ├── Project_Architecture_Document.md # Architecture
    ├── Master_Execution_Plan.md        # 12-phase plan
    └── AGENT.md                        # AI agent handbook
```

### Key Files by Purpose

| Purpose | File | Description |
|---------|------|-------------|
| **GST Calculation** | `billing/models/invoice.py` | `GeneratedField` for GST |
| **PDPA DSAR** | `privacy/models.py` | 72-hour SLA tracking |
| **UEN Validation** | `organizations/models.py` | ACRA regex validation |
| **Idempotency** | `events/models.py` | Duplicate prevention |
| **Stripe Webhooks** | `webhooks/handlers/stripe.py` | Event handling |
| **Singapore Colors** | `tailwind.config.ts` | Red: #eb582d, Blue: #1e3a8a |
| **API Client** | `lib/api/client.ts` | Axios + auth interceptor |

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.12+ | Required |
| Node.js | 20+ | Required |
| PostgreSQL | 16+ | **Required** for GeneratedField |
| Redis | 7.4+ | Cache & Celery broker |

### Quick Start (Docker)

```bash
# Clone repository
git clone https://github.com/nexuscore/platform.git
cd nexuscore

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Access
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# Admin:    http://localhost:8000/admin
```

### Local Development

#### Backend

```bash
cd backend

# Create virtual environment (using uv)
uv venv
source .venv/bin/activate

# Install dependencies
uv sync

# Setup database
createdb nexuscore
python manage.py migrate
python manage.py createsuperuser

# Start server
python manage.py runserver

# Start Celery (in another terminal)
celery -A config worker -Q high,default,low -l INFO
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Environment Variables

```bash
# Backend (.env)
DATABASE_URL=postgres://user:pass@localhost:5432/nexuscore
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=config.settings.development

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# PDPA
PDPA_DSAR_SLA_HOURS=72

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## 📚 API Documentation

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/auth/register/` | User registration |
| `POST` | `/api/v1/auth/login/` | JWT login |
| `GET` | `/api/v1/users/me/` | Current user |
| `GET/POST` | `/api/v1/organizations/` | Organizations (UEN) |
| `GET/POST` | `/api/v1/subscriptions/` | Subscriptions (idempotent) |
| `GET` | `/api/v1/invoices/` | Invoices (GST) |
| `GET/POST` | `/api/v1/leads/` | Leads |
| `GET/POST` | `/api/v1/dsar/` | PDPA DSAR requests |
| `POST` | `/webhooks/stripe/` | Stripe webhooks |
| `GET` | `/health/` | Health check |

### Idempotency

Payment operations require `Idempotency-Key` header:

```bash
curl -X POST https://api.nexuscore.sg/api/v1/subscriptions/ \
  -H "Authorization: Bearer <token>" \
  -H "Idempotency-Key: $(uuidgen)" \
  -H "Content-Type: application/json" \
  -d '{"plan_id": "uuid", "billing_cycle": "monthly"}'
```

---

## 🛤️ User Journey

```mermaid
journey
    title NexusCore User Journey
    
    section Discovery
      Visit Homepage: 5: Visitor
      View Features: 4: Visitor
      Check Pricing: 4: Visitor
    
    section Trial
      Sign Up: 5: New User
      Verify Email: 3: New User
      Complete Onboarding: 4: Trial User
      Add Organization (UEN): 4: Trial User
    
    section Conversion
      Upgrade to Paid: 5: Customer
      Receive Invoice (GST): 5: Customer
      Add Team Members: 4: Customer
    
    section Operations
      Manage Leads: 5: Power User
      View Analytics: 5: Power User
      Submit DSAR Request: 3: Power User
```

---

## 📊 Development Status

### Completed Phases (11/12)

| Phase | Description | Status | Files |
|-------|-------------|--------|-------|
| 1 | Foundation | ✅ | 12 |
| 2 | Infrastructure | ✅ | 9 |
| 3 | User & Auth | ✅ | 9 |
| 4 | Organization & Multi-tenancy | ✅ | 5 |
| 5 | Plans & Subscriptions | ✅ | 4 |
| 6 | Billing & GST Compliance | ✅ | 4 |
| 7 | Lead Management | ✅ | 4 |
| 8 | PDPA & Privacy | ✅ | 4 |
| 9 | Webhooks & Integration | ✅ | 4 |
| 10 | Frontend Foundation | ✅ | 8 |
| 11 | Frontend Pages | ✅ | 20 |
| 12 | Testing & QA | 🔲 | - |

### Database Tables

| Table | App | Singapore Feature |
|-------|-----|-------------------|
| `users` | users | — |
| `organizations` | organizations | UEN, GST Registration |
| `organization_memberships` | organizations | — |
| `plans` | subscriptions | — |
| `subscriptions` | subscriptions | — |
| `invoices` | billing | **GST GeneratedField** |
| `leads` | leads | — |
| `dsar_requests` | privacy | **72-hour SLA** |
| `webhook_events` | webhooks | — |
| `events` | events | — |
| `idempotency_records` | events | — |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript strict mode for frontend
- All GST calculations must use `GeneratedField`
- DSAR operations must respect 72-hour SLA
- Run `ruff check` and `npm run lint` before commits

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built for Singapore 🇸🇬**

NexusCore v4.0 | Database-Level GST | 72-Hour PDPA SLA | UEN Validated

[Website](https://nexuscore.sg) · [Documentation](https://docs.nexuscore.sg) · [API](https://api.nexuscore.sg)

</div>
