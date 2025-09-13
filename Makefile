.PHONY: lock sync lint format mypy unit integration

VENV := .venv
ENV_RUNNER ?= uv
SRC := recommendation_engine

quickstart: init-venv docker-mongo-up run

# --------------------------
# Run (no-docker)
# --------------------------

run:
	@$(ENV_RUNNER) run fastapi dev $(SRC)/main.py --port=8000

# Needed if you need to generate NEW RSA certificates for JWT Authorization
generate_certificates:
	openssl genrsa -out ./conf/cert_private.pem 2048 && openssl rsa -in ./conf/cert_private.pem -pubout -out ./conf/cert_public.pem

# --------------------------
# Run (docker)
# --------------------------
up:
	@docker compose up recommendation-app

down:
	@docker compose down recommendation-app

down-v:
	@docker compose down -v recommendation-app

build:
	@echo 'Building images ...🛠️'
	@docker compose build recommendation-app

docker-app-interactive:
	@docker compose run --rm recommendation-app bash


# ////////////////////
#		DB -- MongoDB
# ////////////////////
docker-mongo-up:
	@docker compose up db-mongodb-dashboard
docker-mongo-down:
	@docker compose down db-mongodb-dashboard
docker-mongo-down-clean-up:
	@docker compose down -v db-mongodb-dashboard

# --------------------------
# Init
# --------------------------
init-venv: update-env-file .install-uv .create-venv update-venv .install-deps
update-venv: lock sync

lock:
	@$(ENV_RUNNER) lock
sync:
	@$(ENV_RUNNER) sync --dev

.install-uv:
	pip install -U uv

.create-venv:
	@if [ -d "./.venv" ]; then \
		echo ".venv python environment exists, skipping..."; \
	else \
		echo ".venv not found, Creating Python environment..."; \
		UV_VENV_CLEAR=1 $(ENV_RUNNER) venv; \
	fi

.install-deps:
	@$(ENV_RUNNER) pip install -e . --group dev

update-env-file:
	@echo 'Updating .env from .env.example 🖋️...'
	@cp .env.example .env
	@echo '.env Updated ✨'

# =========================
# 		Code Quality
# =========================

quality-checks: format lint mypy

lint:
	@$(ENV_RUNNER) run ruff check . --fix
lint-check:
	@$(ENV_RUNNER) run ruff check .

format:
	@$(ENV_RUNNER) run ruff format .
format-check:
	@$(ENV_RUNNER) run ruff format . --check

mypy:
	@$(ENV_RUNNER) run mypy .

# --------------------------
# Tests
# --------------------------
tests: test-unit test-integration

test-unit:
	@$(ENV_RUNNER) run pytest -m unit
test-unit-coverage:
	@$(ENV_RUNNER) run pytest -m unit --cov --cov-report=term-missing --cov-report=html

test-integration:
	@$(ENV_RUNNER) run pytest -m integration
