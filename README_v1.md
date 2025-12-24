# 🚀 NexusCore — Singapore Enterprise SaaS Platform

<div align="center">

![NexusCore](https://img.shields.io/badge/NexusCore-Singapore_SaaS_Platform-eb582d?style=for-the-badge&logo=rocket&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.12+-blue?style=flat-square&logo=python)](https://www.python.org)
[![Django](https://img.shields.io/badge/Django-6.0-green?style=flat-square&logo=django)](https://www.djangoproject.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.2-black?style=flat-square&logo=next.js)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue?style=flat-square&logo=postgresql)](https://www.postgresql.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)

**Enterprise-grade SaaS platform built for Singapore businesses**

GST Compliant • PDPA Ready • UEN Validated

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Singapore Compliance](#-singapore-compliance)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [API Documentation](#-api-documentation)
- [Development Status](#-development-status)

---

## 🌐 Overview

NexusCore v4.0 is a production-ready B2B SaaS platform designed specifically for Singapore businesses. It implements:

- **GST compliance** with database-level calculation
- **PDPA automation** with 72-hour DSAR SLA
- **UEN validation** for all organizations

### Why NexusCore?

| Feature | Benefit |
|---------|---------|
| **🇸🇬 Singapore-First** | Built for local regulatory requirements |
| **📊 GST Compliant** | Automatic 9% calculation with IRAS codes |
| **🔒 PDPA Ready** | 72-hour DSAR handling with approval workflow |
| **⚡ Modern Stack** | Django 6.0 + Next.js 14 |

---

## 🇸🇬 Singapore Compliance

### GST (Goods & Services Tax)

| Requirement | Implementation |
|-------------|----------------|
| Rate | 9% (0.0900) |
| Calculation | **Database-level** via `GeneratedField` |
| IRAS Codes | SR, ZR, OS, TX |
| Currency | SGD (default) |

### PDPA (Personal Data Protection Act)

| Requirement | Implementation |
|-------------|----------------|
| DSAR SLA | 72 hours |
| Deletion | Manual approval required |
| Data Residency | Singapore region |

### UEN (Unique Entity Number)

All organizations must have a valid Singapore UEN:
- Format: `12345678A`, `123456789B`, or `T12AB3456C`

---

## ✨ Features

### Backend (Django 6.0)
- ✅ JWT Authentication with email verification
- ✅ Organization management with UEN/GST
- ✅ Subscription management with Stripe
- ✅ Invoice generation with database-level GST
- ✅ Lead management with UTM tracking
- ✅ DSAR workflow with SLA tracking
- ✅ Stripe webhook handling with idempotency
- ✅ Event logging and audit trail

### Frontend (Next.js 14)
- ✅ Marketing pages (Homepage, Pricing)
- ✅ Auth pages (Login, Signup, Verify)
- ✅ App pages (Dashboard, Leads, Invoices, Settings)
- ✅ Singapore color palette (red: #eb582d, blue: #1e3a8a)
- ✅ Dark mode support
- ✅ Mobile responsive

---

## 💻 Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.12+ | Runtime |
| Django | 6.0 | Web framework |
| Django REST Framework | 3.15+ | API |
| Celery | 5.4+ | Task queue |
| PostgreSQL | 16+ | Database (required for GeneratedField) |
| Redis | 7.4+ | Cache & broker |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 14.2 | React framework |
| React | 18 | UI library |
| TypeScript | 5 | Type safety |
| Tailwind CSS | 3.4 | Styling |
| React Query | 5 | Data fetching |

---

## 📁 Project Structure

```
nexuscore/
├── backend/
│   ├── apps/
│   │   ├── users/           # User authentication
│   │   ├── organizations/   # Organization + UEN/GST
│   │   ├── subscriptions/   # Plans + Stripe
│   │   ├── billing/         # Invoices + GST GeneratedField
│   │   ├── leads/           # Lead management
│   │   ├── privacy/         # DSAR + PDPA
│   │   ├── webhooks/        # Stripe webhooks
│   │   └── events/          # Audit logging
│   ├── config/
│   │   └── settings/        # Django settings
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (marketing)/ # SSG pages
│   │   │   ├── (auth)/      # Auth pages
│   │   │   └── (app)/       # App pages
│   │   ├── components/
│   │   │   ├── ui/          # Button, Input, Card
│   │   │   └── marketing/   # Hero, PricingCard
│   │   ├── lib/
│   │   │   ├── api/         # Axios client
│   │   │   └── providers.tsx
│   │   └── types/
│   │       └── models.ts    # TypeScript types
│   └── tailwind.config.ts   # Singapore colors
└── docs/
    ├── NexusCore-v4.0-Merged-PRD.md
    ├── Project_Architecture_Document.md
    └── Master_Execution_Plan.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL 16+ (required)
- Redis 7.4+

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Setup database
createdb nexuscore

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### Frontend Setup

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
SECRET_KEY=your-secret-key
STRIPE_SECRET_KEY=sk_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## 📚 API Documentation

### Endpoints

| Path | Description |
|------|-------------|
| `/api/v1/auth/` | Authentication |
| `/api/v1/users/` | User management |
| `/api/v1/organizations/` | Organizations (UEN, GST) |
| `/api/v1/subscriptions/` | Subscriptions |
| `/api/v1/invoices/` | Invoices (GST) |
| `/api/v1/leads/` | Lead management |
| `/api/v1/dsar/` | PDPA DSAR requests |
| `/webhooks/stripe/` | Stripe webhooks |

### Idempotency

Payment-related operations require `Idempotency-Key` header:

```bash
curl -X POST /api/v1/subscriptions/ \
  -H "Authorization: Bearer <token>" \
  -H "Idempotency-Key: unique-key-123"
```

---

## 📊 Development Status

### Completed Phases (11/12)

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Foundation | ✅ |
| 2 | Infrastructure | ✅ |
| 3 | User & Auth | ✅ |
| 4 | Organization & Multi-tenancy | ✅ |
| 5 | Plans & Subscriptions | ✅ |
| 6 | Billing & GST Compliance | ✅ |
| 7 | Lead Management | ✅ |
| 8 | PDPA & Privacy | ✅ |
| 9 | Webhooks & Integration | ✅ |
| 10 | Frontend Foundation | ✅ |
| 11 | Frontend Pages | ✅ |
| 12 | Testing & QA | 🔲 |

### Database Tables

| Table | App |
|-------|-----|
| `users` | users |
| `organizations` | organizations |
| `organization_memberships` | organizations |
| `plans` | subscriptions |
| `subscriptions` | subscriptions |
| `invoices` | billing |
| `leads` | leads |
| `dsar_requests` | privacy |
| `webhook_events` | webhooks |
| `events` | events |
| `idempotency_records` | events |

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built for Singapore 🇸🇬**

NexusCore v4.0 | GST Compliant | PDPA Ready

</div>
