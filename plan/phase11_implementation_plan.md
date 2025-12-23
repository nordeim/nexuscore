# Phase 11: Frontend Pages — Implementation Plan

## Goal

Create all pages and components for the NexusCore frontend.

---

## Proposed Changes

### Marketing Pages (`src/app/`)

| File | Purpose |
|------|---------|
| `page.tsx` | **Homepage** with Hero |
| `(marketing)/layout.tsx` | Marketing layout |
| `(marketing)/pricing/page.tsx` | Pricing with GST note |
| `(marketing)/about/page.tsx` | About page |
| `(marketing)/contact/page.tsx` | Contact form |

---

### Auth Pages (`src/app/(auth)/`)

| File | Purpose |
|------|---------|
| `layout.tsx` | Auth layout |
| `login/page.tsx` | Login form |
| `signup/page.tsx` | Signup form |
| `verify/page.tsx` | Email verification |

---

### App Pages (`src/app/(app)/`)

| File | Purpose |
|------|---------|
| `layout.tsx` | App layout + sidebar |
| `dashboard/page.tsx` | Dashboard |
| `leads/page.tsx` | Lead management |
| `invoices/page.tsx` | Invoices with GST |
| `settings/page.tsx` | User settings |

---

### UI Components (`src/components/`)

| Folder | Files |
|--------|-------|
| `ui/` | Button, Input, Card, Modal |
| `marketing/` | Hero, PricingCard |
| `forms/` | LoginForm, SignupForm |

---

## File Count: ~20 Files

---

## Key Requirements

- Singapore colors (`singapore-red`, `singapore-blue`)
- GST note on pricing: "All prices exclude 9% GST"
- Mobile responsive
- Dark mode support

---

## Verification Plan

```bash
npm run build
npm run lint
```

---

## Execution Order

1. Create UI components
2. Create marketing layout + pages
3. Create auth layout + pages
4. Create app layout + pages
5. Build and lint
