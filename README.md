# AI News Aggregator

A modern AI-powered news aggregator built with FastAPI, React 19, Next.js 15, and the latest web technologies.

## Features

- **Backend**: FastAPI with async/await support
- **Frontend**: Next.js 15 with App Router and React 19
- **Database**: PostgreSQL with SQLAlchemy 2.0
- **AI Integration**: OpenAI GPT-4 for summarization
- **Authentication**: JWT-based auth system
- **Testing**: 100% test coverage with pytest
- **Containerization**: Docker & Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for frontend development)  
- Python 3.11+ (for local backend development)
- **uv** - Ultra-fast Python package manager

### Development Setup (Using Makefile)

1. **Clone and setup the project**:
```bash
git clone <your-repo>
cd aiagg
cp backend/.env.example backend/.env
```

2. **Quick development setup**:
```bash
make dev              # Install dependencies + start Docker services
```

3. **Run tests**:
```bash
make test-all         # Run all working tests
```

4. **Start development server**:
```bash
make run-dev          # Start FastAPI server with auto-reload
```

5. **Access the application**:
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Frontend: http://localhost:3000

### Available Make Commands

Get help with all available commands:
```bash
make help              # Show all available commands
```

**Development Workflow:**
```bash
make install-dev       # Install development dependencies
make test-unit         # Run unit tests (core functionality)
make test-api          # Run API tests (FastAPI endpoints)  
make test-all          # Run all working tests
make coverage-html     # Generate HTML coverage report
make lint              # Run code linting
make format            # Format code with ruff
make pre-commit        # Run all code quality checks
```

**Docker Operations:**
```bash
make docker-up         # Start all services
make docker-down       # Stop all services
make docker-logs       # View service logs
make docker-clean      # Clean up containers
```

**Manual Setup (Alternative to Makefile):**
```bash
cd backend
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project with dependencies
uv pip install -e ".[dev]"
cp .env.example .env
# Edit .env with your configuration
uvicorn app.main:app --reload
```

## Project Structure

```
aiagg/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core functionality (config, security)
│   │   ├── db/             # Database models and setup
│   │   ├── services/       # Business logic services
│   │   └── utils/          # Utility functions
│   ├── tests/              # Test suite
│   ├── alembic/            # Database migrations
│   └── pyproject.toml      # Modern Python project config
├── frontend/               # Next.js application (coming soon)
├── docker-compose.yml      # Development environment
└── progress.md            # Development progress tracker
```

## Development Progress

See [progress.md](progress.md) for detailed development progress and continuation instructions.

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /health/` - Basic health check
- `GET /health/db` - Database health check

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login

### Articles (Coming in Phase 2)
- `GET /articles/` - List articles with pagination
- `GET /articles/{id}` - Get specific article

## Technology Stack

- **FastAPI** 0.115+ - Modern Python web framework
- **uv** - Ultra-fast Python package manager (10-100x faster than pip)
- **pyproject.toml** - Modern Python project configuration
- **Pydantic** 2.x - Data validation and settings
- **SQLAlchemy** 2.0 - Database ORM with async support
- **PostgreSQL** - Primary database
- **Redis** - Caching and task queue
- **pytest** 8.x - Testing framework with 100% coverage
- **Ruff** - Lightning-fast Python linter and formatter
- **Docker** - Containerization with uv integration

## Contributing

This project is designed for phased development. Check `progress.md` for current status and next steps.

## License

MIT License