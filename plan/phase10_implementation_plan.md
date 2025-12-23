# Phase 10: Frontend Foundation — Implementation Plan

## Goal

Create Next.js 14 frontend with Tailwind CSS and Elementra design system.

---

## Proposed Changes

### Frontend Setup (`frontend/`)

#### [NEW] Initialize Next.js 14
```bash
npx -y create-next-app@14 ./ --typescript --tailwind --eslint --app --src-dir
```

#### [MODIFY] [tailwind.config.ts](file:///home/project/nexuscore/frontend/tailwind.config.ts)
- Singapore colors (red: #eb582d, blue: #1e3a8a)
- darkMode: 'class'
- Full color scales

#### [MODIFY] [src/app/layout.tsx](file:///home/project/nexuscore/frontend/src/app/layout.tsx)
- QueryClientProvider
- ThemeProvider
- SEO meta tags

#### [NEW] [src/lib/api/client.ts](file:///home/project/nexuscore/frontend/src/lib/api/client.ts)
- Axios instance with auth interceptor
- Idempotency key generator

#### [NEW] [src/types/models.ts](file:///home/project/nexuscore/frontend/src/types/models.ts)
- User, Organization, Invoice, Subscription types
- Match backend exactly

#### [NEW] [src/lib/providers.tsx](file:///home/project/nexuscore/frontend/src/lib/providers.tsx)
- React Query provider
- Theme provider

---

## File Count: ~10 Files (after init)

---

## Singapore Color Palette

| Color | Value |
|-------|-------|
| `singapore.red` | #eb582d |
| `singapore.blue` | #1e3a8a |

---

## Verification Plan

```bash
cd frontend
npm install
npm run build
npm run lint
```

---

## Execution Order

1. Initialize Next.js 14 project
2. Configure Tailwind with Singapore colors
3. Create API client with interceptors
4. Create TypeScript model types
5. Create providers wrapper
6. Update layout with providers
7. Build and lint
