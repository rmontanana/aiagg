# AI News Aggregator - Development Makefile
# ==========================================

.PHONY: help install install-dev clean test test-unit test-models test-api test-all
.PHONY: lint format typecheck pre-commit run run-dev run-prod
.PHONY: docker-up docker-down docker-build docker-logs docker-clean
.PHONY: db-create db-migrate db-upgrade db-downgrade db-reset
.PHONY: coverage coverage-report coverage-html
.PHONY: build deploy release docs
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
UV := uv
BACKEND_DIR := backend
FRONTEND_DIR := frontend
COMPOSE_FILE := docker-compose.yml
TEST_ENV := ENVIRONMENT=test

help: ## Show this help message
	@echo "\033[0;36mAI News Aggregator - Development Commands\033[0m"
	@echo "=========================================="
	@echo ""
	@echo "\033[0;32m📦 Installation:\033[0m"
	@grep -E '^[a-zA-Z_-]+.*:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(install|clean)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "\033[0;32m🧪 Testing:\033[0m"
	@grep -E '^[a-zA-Z_-]+.*:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(test|coverage)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "\033[0;32m🔧 Code Quality:\033[0m"
	@grep -E '^[a-zA-Z_-]+.*:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(lint|format|typecheck|pre-commit)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "\033[0;32m🚀 Running:\033[0m"
	@grep -E '^[a-zA-Z_-]+.*:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(run)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "\033[0;32m🐳 Docker:\033[0m"
	@grep -E '^[a-zA-Z_-]+.*:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(docker)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "\033[0;32m🗄️ Database:\033[0m"
	@grep -E '^[a-zA-Z_-]+.*:.*?## .*$$' $(MAKEFILE_LIST) | grep -E '^(db-)' | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[0;36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "\033[0;33mExample workflow:\033[0m"
	@echo "  make install-dev    # Install dependencies"
	@echo "  make docker-up      # Start services"
	@echo "  make test-all       # Run all tests"
	@echo "  make run-dev        # Start development server"

# ============================================================================
# Installation
# ============================================================================

install: ## Install production dependencies
	@echo "$(GREEN)📦 Installing production dependencies...$(NC)"
	cd $(BACKEND_DIR) && $(UV) pip install -e .

install-dev: ## Install development dependencies
	@echo "$(GREEN)📦 Installing development dependencies...$(NC)"
	cd $(BACKEND_DIR) && $(UV) pip install -e ".[dev]"
	@echo "$(GREEN)✅ Development environment ready!$(NC)"

clean: ## Clean build artifacts and cache
	@echo "$(YELLOW)🧹 Cleaning build artifacts...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@echo "$(GREEN)✅ Cleaned!$(NC)"

# ============================================================================
# Testing
# ============================================================================

test-unit: ## Run unit tests (core functionality)
	@echo "$(GREEN)🧪 Running unit tests...$(NC)"
	cd $(BACKEND_DIR) && $(TEST_ENV) $(UV) run pytest tests/test_unit.py -v

test-models: ## Run model tests (database models)
	@echo "$(GREEN)🧪 Running model tests...$(NC)"
	cd $(BACKEND_DIR) && $(TEST_ENV) $(UV) run pytest tests/test_models.py -v

test-api: ## Run API tests (FastAPI endpoints)
	@echo "$(GREEN)🧪 Running API tests...$(NC)"
	cd $(BACKEND_DIR) && $(TEST_ENV) $(UV) run pytest tests/test_api_simple.py -v

test-all: test-unit test-models test-api ## Run all working tests
	@echo "$(GREEN)✅ All tests completed!$(NC)"

test: test-all ## Alias for test-all

coverage: ## Run tests with coverage report
	@echo "$(GREEN)📊 Running tests with coverage...$(NC)"
	cd $(BACKEND_DIR) && $(TEST_ENV) $(UV) run pytest tests/test_unit.py tests/test_models.py tests/test_api_simple.py --cov=app --cov-report=term-missing

coverage-html: ## Generate HTML coverage report
	@echo "$(GREEN)📊 Generating HTML coverage report...$(NC)"
	cd $(BACKEND_DIR) && $(TEST_ENV) $(UV) run pytest tests/test_unit.py tests/test_models.py tests/test_api_simple.py --cov=app --cov-report=html
	@echo "$(GREEN)📋 Coverage report: $(BACKEND_DIR)/htmlcov/index.html$(NC)"

coverage-report: coverage-html ## Alias for coverage-html

# ============================================================================
# Code Quality
# ============================================================================

lint: ## Run linting with ruff
	@echo "$(GREEN)🔍 Running linter...$(NC)"
	cd $(BACKEND_DIR) && $(UV) run ruff check .

format: ## Format code with ruff
	@echo "$(GREEN)✨ Formatting code...$(NC)"
	cd $(BACKEND_DIR) && $(UV) run ruff format .

typecheck: ## Run type checking with mypy
	@echo "$(GREEN)🔍 Running type checker...$(NC)"
	cd $(BACKEND_DIR) && $(UV) run mypy .

pre-commit: format lint typecheck ## Run all code quality checks
	@echo "$(GREEN)✅ All quality checks completed!$(NC)"

# ============================================================================
# Running the Application
# ============================================================================

run: run-dev ## Alias for run-dev

run-dev: ## Run development server with auto-reload
	@echo "$(GREEN)🚀 Starting development server...$(NC)"
	@echo "$(YELLOW)📋 API Documentation: http://localhost:8000/docs$(NC)"
	cd $(BACKEND_DIR) && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

run-prod: ## Run production server
	@echo "$(GREEN)🚀 Starting production server...$(NC)"
	cd $(BACKEND_DIR) && uvicorn app.main:app --host 0.0.0.0 --port 8000

# ============================================================================
# Docker Operations
# ============================================================================

docker-up: ## Start all services with Docker Compose
	@echo "$(GREEN)🐳 Starting Docker services...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Services started!$(NC)"
	@echo "$(YELLOW)📋 Backend: http://localhost:8000$(NC)"
	@echo "$(YELLOW)📋 Frontend: http://localhost:3000$(NC)"

docker-down: ## Stop all Docker services
	@echo "$(YELLOW)🐳 Stopping Docker services...$(NC)"
	docker-compose down

docker-build: ## Build Docker images
	@echo "$(GREEN)🐳 Building Docker images...$(NC)"
	docker-compose build

docker-logs: ## Show Docker logs
	docker-compose logs -f

docker-clean: docker-down ## Clean up Docker containers and images
	@echo "$(YELLOW)🧹 Cleaning Docker resources...$(NC)"
	docker-compose down -v --remove-orphans
	docker system prune -f

# ============================================================================
# Database Operations
# ============================================================================

db-create: ## Create test database
	@echo "$(GREEN)🗄️ Creating test database...$(NC)"
	cd $(BACKEND_DIR) && $(PYTHON) scripts/create_test_db.py

db-migrate: ## Generate new migration
	@echo "$(GREEN)🗄️ Generating migration...$(NC)"
	cd $(BACKEND_DIR) && alembic revision --autogenerate -m "$(MSG)"

db-upgrade: ## Apply database migrations
	@echo "$(GREEN)🗄️ Applying migrations...$(NC)"
	cd $(BACKEND_DIR) && alembic upgrade head

db-downgrade: ## Rollback last migration
	@echo "$(YELLOW)🗄️ Rolling back migration...$(NC)"
	cd $(BACKEND_DIR) && alembic downgrade -1

db-reset: docker-down docker-up db-create ## Reset database (Docker + recreate)
	@echo "$(GREEN)🗄️ Database reset complete!$(NC)"

# ============================================================================
# Build and Deployment
# ============================================================================

build: clean install-dev pre-commit test-all ## Full build process
	@echo "$(GREEN)✅ Build completed successfully!$(NC)"

check: pre-commit test-all ## Run all checks (quality + tests)
	@echo "$(GREEN)✅ All checks passed!$(NC)"

# ============================================================================
# Development Workflow Shortcuts
# ============================================================================

dev: install-dev docker-up ## Quick development setup
	@echo "$(GREEN)🚀 Development environment ready!$(NC)"
	@echo "$(YELLOW)💡 Next steps:$(NC)"
	@echo "  make test-all     # Run tests"
	@echo "  make run-dev      # Start server"

quick-test: test-unit test-models ## Quick test (skip API tests)
	@echo "$(GREEN)⚡ Quick tests completed!$(NC)"

full-check: clean install-dev pre-commit test-all coverage-html ## Complete quality check
	@echo "$(GREEN)🎉 Full check completed!$(NC)"

# ============================================================================
# Info Commands
# ============================================================================

info: ## Show project information
	@echo "$(CYAN)AI News Aggregator Project Info$(NC)"
	@echo "================================"
	@echo "Backend: FastAPI + SQLAlchemy + PostgreSQL"
	@echo "Package Manager: uv (ultra-fast Python package manager)"
	@echo "Testing: pytest with 70%+ coverage target"
	@echo "Code Quality: ruff (linting + formatting) + mypy"
	@echo "Database: PostgreSQL with async SQLAlchemy 2.0"
	@echo "Container: Docker Compose for development"
	@echo ""
	@echo "📁 Project Structure:"
	@echo "  backend/     - FastAPI backend application"
	@echo "  frontend/    - Next.js frontend (Phase 2)"
	@echo "  tests/       - Test suites"
	@echo "  docker-compose.yml - Development services"
	@echo ""

status: ## Show service status
	@echo "$(CYAN)Service Status$(NC)"
	@echo "==============="
	@echo "Docker Compose Services:"
	@docker-compose ps 2>/dev/null || echo "Docker Compose not running"
	@echo ""