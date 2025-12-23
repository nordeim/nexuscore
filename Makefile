# NexusCore v4.0 - Makefile
# Common commands for development and deployment

.PHONY: help up down build logs shell migrate test lint format

# Default target
help:
	@echo "NexusCore Development Commands"
	@echo "=============================="
	@echo "  make up        - Start all services"
	@echo "  make down      - Stop all services"
	@echo "  make build     - Build all images"
	@echo "  make logs      - View logs"
	@echo "  make shell     - Django shell"
	@echo "  make migrate   - Run migrations"
	@echo "  make test      - Run tests"
	@echo "  make lint      - Run linters"
	@echo "  make format    - Format code"

# Docker commands
up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

# Backend commands
shell:
	docker compose exec backend python manage.py shell

migrate:
	docker compose run --rm backend python manage.py migrate

makemigrations:
	docker compose run --rm backend python manage.py makemigrations

test:
	docker compose run --rm backend pytest

test-cov:
	docker compose run --rm backend pytest --cov=apps --cov-report=html

# Code quality
lint:
	docker compose run --rm backend ruff check .
	cd frontend && npm run lint

format:
	docker compose run --rm backend ruff format .
	cd frontend && npm run format

# Database
psql:
	docker compose exec postgres psql -U nexuscore_user nexuscore

# Celery
celery-logs:
	docker compose logs -f celery

# Cleanup
clean:
	docker compose down -v --remove-orphans
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Setup
setup:
	cp .env.example .env
	docker compose build
	docker compose up -d postgres redis
	sleep 5
	docker compose run --rm backend python manage.py migrate
	docker compose up -d
	@echo "✅ Setup complete! Visit http://localhost:3000"
