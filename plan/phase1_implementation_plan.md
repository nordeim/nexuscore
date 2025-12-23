# Phase 1: Project Foundation — Implementation Plan

## Goal

Create the complete project scaffolding and Docker environment for NexusCore v4.0, enabling subsequent phases to build upon a stable foundation.

---

## Proposed Changes

### Root Project Structure

#### [NEW] [docker-compose.yml](file:///home/project/nexuscore/docker-compose.yml)
- 7 services: nginx, backend, frontend, celery, postgres, redis, mailpit
- PostgreSQL 16, Redis 7.4
- Network: nexuscore-network
- Volume: postgres_data

#### [NEW] [.env.example](file:///home/project/nexuscore/.env.example)
- All environment variables from PAD Section 7.2
- Singapore region: ap-southeast-1
- PDPA_DSAR_SLA_HOURS=72

#### [NEW] [Makefile](file:///home/project/nexuscore/Makefile)
- Common commands: up, down, migrate, test, shell

---

### Backend Structure

#### [NEW] [backend/Dockerfile](file:///home/project/nexuscore/backend/Dockerfile)
- Python 3.12-slim base
- Non-root user
- PYTHONDONTWRITEBYTECODE=1, PYTHONUNBUFFERED=1

#### [NEW] [backend/requirements/base.txt](file:///home/project/nexuscore/backend/requirements/base.txt)
- Django>=6.0, psycopg[binary]>=3.1, redis>=5.0, celery>=5.4

#### [NEW] [backend/requirements/development.txt](file:///home/project/nexuscore/backend/requirements/development.txt)
- Extends base.txt with pytest, black, ruff

#### [NEW] [backend/manage.py](file:///home/project/nexuscore/backend/manage.py)
- Settings module: config.settings

#### [NEW] [backend/config/__init__.py](file:///home/project/nexuscore/backend/config/__init__.py)
- Exports celery_app

#### [NEW] [backend/config/celery.py](file:///home/project/nexuscore/backend/config/celery.py)
- Task queues: high, default, low
- Timezone: Asia/Singapore

#### [NEW] [backend/config/urls.py](file:///home/project/nexuscore/backend/config/urls.py)
- Admin at /admin/
- API at /api/v1/
- Health check at /health/

#### [NEW] [backend/config/settings/base.py](file:///home/project/nexuscore/backend/config/settings/base.py)
- CONN_HEALTH_CHECKS=True
- AUTH_USER_MODEL='users.User'
- TIME_ZONE='Asia/Singapore'

#### [NEW] [backend/config/settings/__init__.py](file:///home/project/nexuscore/backend/config/settings/__init__.py)
- Empty package file

---

## File Count: 12 Files

| Category | Files |
|----------|-------|
| Root | 3 (docker-compose.yml, .env.example, Makefile) |
| Backend Docker | 1 (Dockerfile) |
| Backend Requirements | 2 (base.txt, development.txt) |
| Backend Config | 6 (manage.py, __init__.py, celery.py, urls.py, settings/base.py, settings/__init__.py) |

---

## Verification Plan

### Automated Verification

#### 1. Docker Compose Syntax Validation
```bash
cd /home/project/nexuscore
docker compose config
```
**Expected**: No errors, full config displayed

#### 2. Docker Build
```bash
cd /home/project/nexuscore
docker compose build backend
```
**Expected**: Image builds successfully with Python 3.12

#### 3. Django Syntax Check
```bash
cd /home/project/nexuscore
docker compose run --rm backend python manage.py check
```
**Expected**: "System check identified no issues"

### Manual Verification

1. **Verify PostgreSQL Version**: 
   - In docker-compose.yml, confirm `image: postgres:16`

2. **Verify Singapore Region**: 
   - In .env.example, confirm `AWS_S3_REGION_NAME=ap-southeast-1`

3. **Verify PDPA SLA**: 
   - In .env.example, confirm `PDPA_DSAR_SLA_HOURS=72`

4. **Verify Celery Queues**: 
   - In config/celery.py, confirm three queues: high, default, low

---

## Execution Order

1. Create directory structure
2. Create docker-compose.yml
3. Create .env.example
4. Create Makefile
5. Create backend/Dockerfile
6. Create backend/requirements/*.txt
7. Create backend/manage.py
8. Create backend/config/__init__.py
9. Create backend/config/celery.py
10. Create backend/config/urls.py
11. Create backend/config/settings/__init__.py
12. Create backend/config/settings/base.py
13. **Validate** with `docker compose config`
