# Repository Guidelines

## Project Structure & Module Organization
- `backend/` FastAPI app: `app/api` (routes), `app/core` (config, security), `app/db` (models, alembic), `services/`, `utils/`, `tests/`.
- `frontend/` Next.js scaffold (phase 2).
- `docker-compose.yml` Postgres, Redis, backend; local dev via Make targets.

## Build, Test, and Development Commands
- `make install-dev` Install backend dev deps with `uv`.
- `make run-dev` Start FastAPI on `:8000` with auto‑reload; docs at `/docs`.
- `make test-all` Run all tests; `make test-unit|test-api|test-models` for subsets.
- `make lint` Ruff lint; `make format` Ruff formatter; `make typecheck` mypy.
- `make docker-up|docker-down|docker-logs` Manage services; `make db-migrate MSG="msg"`, `make db-upgrade` for alembic.
- Quick setup: `make dev` (install + Docker up). Full check: `make check` or `make full-check`.

## Coding Style & Naming Conventions
- Python 3.11+, 4‑space indentation, max line length 88 (ruff). Use type hints.
- Naming: modules/files `snake_case.py`, classes `PascalCase`, functions/vars `snake_case`.
- Imports: grouped/sorted (ruff “I”). Avoid unused imports; prefer explicit exports.
- Configuration via `backend/.env` (copy from `.env.example`). Do not commit secrets.

## Testing Guidelines
- Framework: `pytest` with async support; coverage target ≥ 70% (see `pyproject.toml`).
- Location: `backend/tests/`; name tests `test_*.py`; mark with `@pytest.mark.unit|integration|slow|simple` as appropriate.
- Commands: `make test-all`, or focused files with `uv run pytest tests/test_api_simple.py -v` from `backend/`.
- Reports: `make coverage-html` generates `backend/htmlcov/index.html`.

## Commit & Pull Request Guidelines
- Commits: imperative mood, concise subject, descriptive body when needed (e.g., “Add auth route and tests”). Reference issues (`#123`).
- PRs: include summary, scope, test coverage notes, and screenshots/logs for UX/API changes. Keep PRs focused and small.
- CI: ensure `make check` passes locally; resolve lint/type errors before review.

## Security & Configuration Tips
- Use Docker services for local DB/Redis: `make docker-up`. Migrate before testing: `make db-upgrade` or `make db-test-setup`.
- Rotate `SECRET_KEY` in production. Validate `/health` and `/health/db` endpoints after changes.

## Agent-Specific Instructions
- Follow these guidelines’ scope for all files. Prefer Make targets over ad‑hoc commands. Avoid unrelated refactors, and run `make pre-commit` before opening a PR.

