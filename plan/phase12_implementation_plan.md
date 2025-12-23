# Phase 12: Testing & Production — Implementation Plan

## Goal

Create test suites, production Docker config, and CI/CD pipeline.

---

## Proposed Changes

### Backend Tests (`backend/tests/`)

#### [NEW] [test_merge_validation.py](file:///home/project/nexuscore/backend/tests/test_merge_validation.py)
- test_idempotency_record_exists
- test_webhook_event_exists
- test_gst_generated_field
- test_uen_validation
- test_singapore_timezone

#### [NEW] [test_gst_compliance.py](file:///home/project/nexuscore/backend/tests/test_gst_compliance.py)
- test_gst_calculation_accuracy
- test_iras_transaction_codes
- test_gst_rounding
- test_zero_rate_gst

---

### Production Config

#### [NEW] [docker-compose.prod.yml](file:///home/project/nexuscore/docker-compose.prod.yml)
- Gunicorn with workers
- Health checks
- Resource limits

#### [NEW] [.github/workflows/ci.yml](file:///home/project/nexuscore/.github/workflows/ci.yml)
- Python tests (pytest)
- Frontend tests
- Linting (ruff, eslint)

---

## File Count: 4 Files

---

## Verification Plan

```bash
# Run tests
cd backend && uv run pytest tests/ -v

# Validate production config
docker-compose -f docker-compose.prod.yml config
```

---

## Execution Order

1. Create tests/__init__.py
2. Create test_merge_validation.py
3. Create test_gst_compliance.py
4. Create docker-compose.prod.yml
5. Create .github/workflows/ci.yml
6. Run tests
