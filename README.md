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

### Development Setup

1. **Clone and setup the project**:
```bash
git clone <your-repo>
cd aiagg
cp backend/.env.example backend/.env
```

2. **Start services with Docker Compose**:
```bash
docker-compose up -d
```

3. **Run database migrations**:
```bash
docker-compose exec backend alembic upgrade head
```

4. **Access the application**:
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Frontend: http://localhost:3000

### Local Development

**Backend**:
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
uvicorn app.main:app --reload
```

**Testing**:
```bash
cd backend
pytest
# For coverage report:
pytest --cov=app --cov-report=html
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
│   └── requirements.txt    # Python dependencies
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
- **Pydantic** 2.x - Data validation and settings
- **SQLAlchemy** 2.0 - Database ORM
- **PostgreSQL** - Primary database
- **Redis** - Caching and task queue
- **pytest** 8.x - Testing framework
- **Docker** - Containerization

## Contributing

This project is designed for phased development. Check `progress.md` for current status and next steps.

## License

MIT License