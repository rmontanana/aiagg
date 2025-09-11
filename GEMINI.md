# GEMINI.md - AI News Aggregator

## Project Overview

This project is an AI-powered news aggregator with a FastAPI backend and a Next.js/React frontend. The backend is well-developed and includes features like a robust testing suite, database migrations, and asynchronous operations. The frontend is not yet implemented.

**Key Technologies:**

*   **Backend:** FastAPI, SQLAlchemy 2.0, PostgreSQL, Redis
*   **Frontend:** Next.js 15, React 19 (planned)
*   **Testing:** pytest
*   **Containerization:** Docker, Docker Compose
*   **Package Management:** uv (Python), npm (Node.js)

**Architecture:**

The application is composed of three main services:

*   **`backend`:** A FastAPI application that provides a RESTful API for managing news articles.
*   **`db`:** A PostgreSQL database that stores the application's data.
*   **`redis`:** A Redis instance used for caching and other tasks.

The services are managed using Docker Compose, which simplifies the development and deployment process.

## Building and Running

The project uses a `Makefile` to provide a convenient set of commands for building, running, and testing the application.

**Key Commands:**

*   `make dev`: Installs dependencies and starts the Docker services.
*   `make test-all`: Runs all tests.
*   `make run-dev`: Starts the FastAPI development server with auto-reload.
*   `make docker-up`: Starts all services with Docker Compose.
*   `make docker-down`: Stops all Docker services.

**Development Workflow:**

1.  **Install dependencies:** `make install-dev`
2.  **Start services:** `make docker-up`
3.  **Run tests:** `make test-all`
4.  **Start development server:** `make run-dev`

## Development Conventions

*   **Asynchronous Code:** The backend extensively uses `async/await` for asynchronous operations, which is a core feature of FastAPI.
*   **Dependency Injection:** FastAPI's dependency injection system is used to manage dependencies, such as the database session.
*   **Configuration:** The application's configuration is managed using Pydantic's `BaseSettings` and loaded from environment variables.
*   **Testing:** The project has a comprehensive test suite with a high level of test coverage. Tests are organized by type (unit, API, etc.) and can be run individually or all at once.
*   **Database Migrations:** Alembic is used to manage database schema migrations.
*   **Linting and Formatting:** Ruff is used for linting and code formatting.
*   **Type Checking:** mypy is used for static type checking.
