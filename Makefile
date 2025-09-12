# AI News Aggregator - Development Makefile
# ==========================================

.PHONY: help install install-dev clean test test-unit test-models test-api test-all test-by-category test-coverage
.PHONY: lint format typecheck pre-commit run run-dev run-prod
.PHONY: docker-up docker-down docker-build docker-logs docker-clean
.PHONY: db-create db-migrate db-upgrade db-downgrade db-reset
.PHONY: coverage coverage-report coverage-html
.PHONY: build deploy release docs info status
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
UV := uv
BACKEND_DIR := backend
FRONTEND_DIR := frontend
COMPOSE_FILE := docker-compose.yml
TEST_ENV := ENVIRONMENT=test
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
CYAN := \033[0;36m
NC := \033[0m

help: ## Show this help message
	@printf "$(BLUE)AI News Aggregator - Development Commands\n"
	@printf "==========================================$(NC)\n"
	@printf "$(BLUE)📦 Installation:$(NC)\n"
	@grep -E '^[a-zA-Z_-]+.*:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(install|clean)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@printf "\n"
	@printf "$(BLUE)🧪 Testing:$(NC)\n"
	@grep -E '^[a-zA-Z_-]+.*:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(test|coverage)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@printf "\n"
	@printf "$(BLUE)🔧 Code Quality:$(NC)\n"
	@grep -E '^[a-zA-Z_-]+.*:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(lint|format|typecheck|pre-commit)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@printf "\n"
	@printf "$(BLUE)🚀 Running:$(NC)\n"
	@grep -E '^[a-zA-Z_-]+.*:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(run)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@printf "\n"
	@printf "$(BLUE)🐳 Docker:$(NC)\n"
	@grep -E '^[a-zA-Z_-]+.*:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(docker)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@printf "\n"
	@printf "$(BLUE)🗄️ Database:$(NC)\n"
	@grep -E '^[a-zA-Z_-]+.*:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(db-)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@printf "\n"
	@printf "$(BLUE)ℹ️ Info & Status:$(NC)\n"
	@grep -E '^[a-zA-Z_-]+.*:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(info|status)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@printf "\n"
	@printf "$(YELLOW)Example workflow:$(NC)\n"
	@printf "  make install-dev    # Install dependencies\n"
	@printf "  make docker-up      # Start services\n"
	@printf "  make test-all       # Run all tests\n"
	@printf "  make run-dev        # Start development server\n"

# ============================================================================
# Installation
# ============================================================================

install: ## Install production dependencies
	@printf "$(GREEN)📦 Installing production dependencies...$(NC)\n"
	cd $(BACKEND_DIR) && $(UV) pip install -e .

install-dev: ## Install development dependencies
	@printf "$(GREEN)📦 Installing development dependencies...$(NC)\n"
	cd $(BACKEND_DIR) && $(UV) pip install -e ".[dev]"
	@printf "$(GREEN)✅ Development environment ready!$(NC)\n"

clean: ## Clean build artifacts and cache
	@printf "$(YELLOW)🧹 Cleaning build artifacts...$(NC)\n"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@printf "$(GREEN)✅ Cleaned!$(NC)\n"

# ============================================================================
# Testing
# ============================================================================

test-unit: ## Run unit tests (core functionality)
	@printf "$(GREEN)🧪 Running unit tests...$(NC)\n"
	cd $(BACKEND_DIR) && $(TEST_ENV) $(UV) run pytest tests/test_unit.py -v --cov-fail-under=0

test-models: ## Run model tests (database models)
	@printf "$(GREEN)🧪 Running model tests...$(NC)\n"
	cd $(BACKEND_DIR) && $(TEST_ENV) $(UV) run pytest tests/test_models.py -v --cov-fail-under=0

test-api: ## Run API tests (FastAPI endpoints)
	@printf "$(GREEN)🧪 Running API tests...$(NC)\n"
	cd $(BACKEND_DIR) && $(TEST_ENV) $(UV) run pytest tests/test_api_simple.py -v --cov-fail-under=0

test-coverage: ## Run comprehensive coverage tests
	@printf "$(GREEN)🧪 Running comprehensive coverage tests...$(NC)\n"
	cd $(BACKEND_DIR) && $(TEST_ENV) $(UV) run pytest tests/test_security_extended.py tests/test_dependencies.py tests/test_database.py tests/test_health_extended.py -v --cov-fail-under=0

test-auth: ## Run authentication tests
	@printf "$(GREEN)🧪 Running authentication tests...$(NC)\n"
	cd $(BACKEND_DIR) && $(TEST_ENV) $(UV) run pytest tests/test_auth_comprehensive.py -v --cov-fail-under=0

test-all: ## Run all tests in one command
	@printf "$(GREEN)🧪 Running all tests...$(NC)\n"
	cd $(BACKEND_DIR) && $(TEST_ENV) $(UV) run pytest tests -v
	@printf "$(GREEN)✅ All tests completed!$(NC)\n"

test-with-db-setup: db-test-setup test-all ## Run tests with fresh test database
	@printf "$(GREEN)✅ Tests completed with fresh database!$(NC)\n"

test: test-all ## Alias for test-all

test-by-category: test-unit test-models test-api test-coverage ## Run tests by category (legacy)
	@printf "$(GREEN)✅ All categorized tests completed!$(NC)\n"

coverage: ## Run tests with coverage report
	@printf "$(GREEN)📊 Running tests with coverage...$(NC)\n"
	cd $(BACKEND_DIR) && $(TEST_ENV) $(UV) run pytest tests --cov=app --cov-report=term-missing

coverage-html: ## Generate HTML coverage report
	@printf "$(GREEN)📊 Generating HTML coverage report...$(NC)\n"
	cd $(BACKEND_DIR) && $(TEST_ENV) $(UV) run pytest tests --cov=app --cov-report=html
	@printf "$(GREEN)📋 Coverage report: $(BACKEND_DIR)/htmlcov/index.html$(NC)"

coverage-report: coverage-html ## Alias for coverage-html

# ============================================================================
# Code Quality
# ============================================================================

lint: ## Run linting with ruff
	@printf "$(GREEN)🔍 Running linter...$(NC)\n"
	cd $(BACKEND_DIR) && $(UV) run ruff check .

format: ## Format code with ruff
	@printf "$(GREEN)✨ Formatting code...$(NC)\n"
	cd $(BACKEND_DIR) && $(UV) run ruff format .

typecheck: ## Run type checking with mypy
	@printf "$(GREEN)🔍 Running type checker...$(NC)\n"
	cd $(BACKEND_DIR) && $(UV) run mypy .

pre-commit: format lint typecheck ## Run all code quality checks
	@printf "$(GREEN)✅ All quality checks completed!$(NC)\n"

# ============================================================================
# Running the Application
# ============================================================================

run: run-dev ## Alias for run-dev

run-dev: ## Run development server with auto-reload
	@printf "$(GREEN)🚀 Starting development server...$(NC)\n"
	@printf "$(YELLOW)📋 API Documentation: http://localhost:8000/docs$(NC)"
	cd $(BACKEND_DIR) && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run-prod: ## Run production server
	@printf "$(GREEN)🚀 Starting production server...$(NC)\n"
	cd $(BACKEND_DIR) && uvicorn app.main:app --host 0.0.0.0 --port 8000

# ============================================================================
# Docker Operations
# ============================================================================

docker-up: ## Start all services with Docker Compose
	@printf "$(GREEN)🐳 Starting Docker services...$(NC)\n"
	docker compose up -d
	@printf "$(GREEN)✅ Services started!$(NC)\n"
	@printf "$(YELLOW)📋 Backend: http://localhost:8000$(NC)\n"
	@printf "$(YELLOW)📋 Frontend: http://localhost:3000$(NC)\n"

docker-down: ## Stop all Docker services
	@printf "$(YELLOW)🐳 Stopping Docker services...$(NC)\n"
	docker compose down

docker-build: ## Build Docker images
	@printf "$(GREEN)🐳 Building Docker images...$(NC)\n"
	docker compose build

docker-logs: ## Show Docker logs
	docker compose logs -f

docker-clean: docker-down ## Clean up Docker containers and images
	@printf "$(YELLOW)🧹 Cleaning Docker resources...$(NC)\n"
	docker compose down -v --remove-orphans
	docker system prune -f

# ============================================================================
# Database Operations
# ============================================================================

db-migrate: ## Generate new migration
	@printf "$(GREEN)🗄️ Generating migration...$(NC)\n"
	cd $(BACKEND_DIR) && alembic revision --autogenerate -m "$(MSG)"

db-upgrade: ## Apply database migrations
	@printf "$(GREEN)🗄️ Applying migrations...$(NC)\n"
	cd $(BACKEND_DIR) && alembic upgrade head

db-downgrade: ## Rollback last migration
	@printf "$(YELLOW)🗄️ Rolling back migration...$(NC)\n"
	cd $(BACKEND_DIR) && alembic downgrade -1

db-test-setup: ## Setup test database with migrations (Docker)
	@printf "$(GREEN)🗄️ Creating test database...$(NC)\n"
	cd $(BACKEND_DIR) && $(PYTHON) scripts/create_test_db.py
	@printf "$(GREEN)🗄️ Setting up test database...$(NC)\n"
	docker exec backend sh -c "ENVIRONMENT=test DATABASE_URL=postgresql://postgres:postgres@db:5432/aiagg_test alembic downgrade base || true"
	docker exec backend sh -c "ENVIRONMENT=test DATABASE_URL=postgresql://postgres:postgres@db:5432/aiagg_test alembic upgrade head"
	@printf "$(GREEN)✅ Test database ready!$(NC)\n"

db-reset: docker-down docker-up db-create ## Reset database (Docker + recreate)
	@printf "$(GREEN)🗄️ Database reset complete!$(NC)\n"

# ============================================================================
# Build and Deployment
# ============================================================================

build: clean install-dev pre-commit test-all ## Full build process
	@printf "$(GREEN)✅ Build completed successfully!$(NC)\n"

check: pre-commit test-all ## Run all checks (quality + tests)
	@printf "$(GREEN)✅ All checks passed!$(NC)\n"

# ============================================================================
# Development Workflow Shortcuts
# ============================================================================

dev: install-dev docker-up ## Quick development setup
	@printf "$(GREEN)🚀 Development environment ready!$(NC)\n"
	@printf "$(YELLOW)💡 Next steps:$(NC)\n"
	@printf "  make test-all     # Run tests\n"
	@printf "  make run-dev      # Start server\n"

quick-test: test-unit test-models ## Quick test (skip API tests)
	@printf "$(GREEN)⚡ Quick tests completed!$(NC)\n"

full-check: clean install-dev pre-commit test-all coverage-html ## Complete quality check
	@printf "$(GREEN)🎉 Full check completed!$(NC)\n"

# ============================================================================
# Info Commands
# ============================================================================

info: ## Show project information
	@printf "$(CYAN)AI News Aggregator Project Info\n"
	@printf "================================$(NC)\n"
	@printf "Backend: FastAPI + SQLAlchemy + PostgreSQL\n"
	@printf "Package Manager: uv (ultra-fast Python package manager)\n"
	@printf "Testing: pytest with 70%+ coverage target\n"
	@printf "Code Quality: ruff (linting + formatting) + mypy\n"
	@printf "Database: PostgreSQL with async SQLAlchemy 2.0\n"
	@printf "Container: Docker Compose for development\n"
	@printf "📁 Project Structure:\n"
	@printf "  backend/     - FastAPI backend application\n"
	@printf "  frontend/    - Next.js frontend (Phase 2)\n"
	@printf "  tests/       - Test suites\n"
	@printf "  docker-compose.yml - Development services\n"

status: ## Show service status
	@printf "$(CYAN)Service Status\n"
	@printf "===============$(NC)\n"
	@printf "Docker Compose Services:\n"
	@docker compose ps 2>/dev/null || echo "Docker Compose not running"
	@printf "\n"
