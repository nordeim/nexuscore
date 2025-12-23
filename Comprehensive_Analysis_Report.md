Please meticulously plan and perform a deep-dive analysis of the attached project documents (`PAD-Validation-Analysis.md`, `PRD-qd-3-appendix.md`, `Project_Architecture_Document.md`, and `NexusCore-v4.0-Merged-PRD.md`). Then create a comprehensive analysis report detailing the **WHAT**, **WHY**, and **HOW** of project. Next, validate your analysis and understanding with the following analysis.

## 1. Executive Summary
NexusCore v4.0 is a **Singapore-first B2B SaaS platform** designed to be production-ready immediately upon deployment. It is not merely a feature update but a strategic architectural merger of two distinct predecessor specifications:
1.  **PRD-d-3 (Infrastructure):** Provided the operational backbone (Idempotency, Webhooks, Event Logging).
2.  **PRD-q-3 (Domain Logic):** Provided the Singaporean regulatory logic (GST, UEN, PDPA).

**The Critical Insight:** A "Strict Merge" strategy was required because `PRD-q-3` (the domain layer) silently depended on models (like `IdempotencyRecord`) that were only defined in `PRD-d-3`. Without this merge, the application would have failed at runtime.

---

## 2. Strategic Context (The WHY)

The project aims to solve specific regulatory and operational challenges in the Singapore market that generic SaaS templates fail to address.

| Dimension | Requirement | Implementation Strategy |
|:---|:---|:---|
| **Regulatory** | **GST Compliance** | Fixed 9% GST calculated at the **Database Layer** to prevent application-level floating-point drift. |
| **Identity** | **UEN Validation** | Strict Regex validation against ACRA formats (e.g., `T12LL1234A`) to ensure B2B legitimacy. |
| **Privacy** | **PDPA / DSAR** | Automated 72-hour SLA tracking for Data Subject Access Requests with manual approval gates for deletion. |
| **Reliability** | **Idempotency** | Prevention of duplicate payments/requests via a dedicated `IdempotencyRecord` framework. |

---

## 3. Technical Architecture (The HOW)

The stack is modernized to **Django 6.0** and **Next.js 14**, leveraging the latest features for performance and type safety.

### 3.1 Backend Architecture (Django 6.0)
The backend is a "Modular Monolith" designed for immediate stability and future scalability.

*   **Database-Level Logic (Crucial):**
    The system utilizes Django 6.0's `GeneratedField` to map to PostgreSQL 16's `GENERATED ALWAYS AS` columns.
    ```python
    # From NexusCore-v4.0-Merged-PRD.md
    gst_amount_cents = models.GeneratedField(
        expression=models.Func(
            models.F('subtotal_cents') * models.F('gst_rate'),
            function='ROUND',
            output_field=models.BigIntegerField()
        ),
        output_field=models.BigIntegerField(),
        db_persist=True
    )
    ```
    *Why this matters:* It creates an immutable audit trail. Even if the API code changes, the database guarantees the tax calculation remains consistent with the data at rest.

*   **Async Capabilities:**
    The architecture leverages Django 6.0's native async support (`aget`, `acreate`) combined with Celery for heavy lifting (PDF generation, webhooks).

*   **Missing Dependencies Resolved:**
    The analysis confirms the inclusion of `IdempotencyRecord` and `WebhookEvent` models, which were identified as critical missing links in `PRD-qd-3-appendix.md`.

### 3.2 Frontend Architecture (Next.js 14)
*   **Design System:** "Elementra" adapted for Singapore (e.g., using specific hex codes like `#eb582d` for Singapore Red).
*   **Performance:** Strict budgets (Mobile LCP ≤2.5s).
*   **Structure:** App Router with clear separation of Marketing (SSG) and Application (SSR) routes.

### 3.3 Infrastructure (Production Ready)
*   **Containerization:** Full Docker Compose setup including Nginx, Postgres 16, Redis 7.4.
*   **Security:**
    *   Native CSP (Content Security Policy) middleware.
    *   Connection health checks (`CONN_HEALTH_CHECKS = True`).
    *   Data Residency: Enforced `ap-southeast-1` (Singapore) for AWS S3.

---

## 4. Implementation Phase Analysis

The project follows a strict 13-week timeline divided into four phases. Based on the "Strict Merge Strategy," the implementation order is non-negotiable.

### Phase 1: Foundation (Weeks 1-4)
*   **Focus:** Core Infrastructure (PRD-d-3).
*   **Critical Action:** We must implement the "Foundation Layer" first. This means `IdempotencyRecord`, `WebhookEvent`, and `Event` models must exist *before* we try to build the Subscription logic that relies on them.

### Phase 2: Compliance Engine (Weeks 5-7)
*   **Focus:** Domain Logic (PRD-q-3).
*   **Critical Action:** Implementing the `Organization` model with UEN validation and the `Invoice` model with GST `GeneratedFields`.

### Phase 3: Payments & Integration (Weeks 8-9)
*   **Focus:** Merging the two.
*   **Critical Action:** Wiring Stripe Webhooks (Infrastructure) to generate GST-Compliant Invoices (Domain).

### Phase 4: Hardening (Weeks 10-13)
*   **Focus:** Security and SLA.
*   **Critical Action:** Validating DSAR workflows and ensuring the 72-hour automated retention policies work via Celery beat.

---

## 5. Risk Assessment & Mitigation

Based on my analysis of the `PRD-qd-3-appendix.md` and the `PAD-Validation-Analysis.md`, here are the top risks I will actively manage:

1.  **The "Silent Failure" Risk:**
    *   *Risk:* Using `PRD-q-3` logic without `PRD-d-3` models causes `NameError`.
    *   *Mitigation:* I will enforce the "Strict Merge" by implementing the infrastructure models (Idempotency/Webhooks) in `apps/core` immediately.

2.  **Tailwind Configuration Drift:**
    *   *Risk:* `PRD-q-3` components use `singapore-red` but `PRD-d-3` config doesn't define it.
    *   *Mitigation:* I will verify `tailwind.config.js` includes the specific Singapore color palette defined in the merged PRD.

3.  **Database Version Incompatibility:**
    *   *Risk:* `GeneratedField` requires PostgreSQL 16+.
    *   *Mitigation:* I will ensure the Docker configuration strictly pins `postgres:16-alpine`.

---

## 6. Conclusion

The documents provide a remarkably complete and high-quality blueprint. The "Strict Merge" was the correct strategic decision. We have:
*   **Clear Data Models:** 100% defined.
*   **Clear Compliance Rules:** Regex and Logic are explicit.
*   **Clear Infrastructure:** Docker and Env vars are documented.

