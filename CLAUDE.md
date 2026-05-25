# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Python is managed with **uv**, dependencies declared in `pyproject.toml` (requires Python >=3.12). Backend imports are package-rooted at the repo root (e.g. `from api.product_api import ...`), so commands must be run from the project root.

Backend:
- Install deps: `uv sync`
- Run API (dev, with reload): `uv run uvicorn main:app --reload` — serves on `http://localhost:8000`
- Run all tests: `uv run python -m pytest -v`
- Run a single test: `uv run python -m pytest tests/test_product_api.py::test_get_all_products -v`

Frontend (in `frontend/`):
- Install: `npm install`
- Dev server: `npm start` — serves on `http://localhost:3000`, proxies to backend at `localhost:8000` (see `frontend/package.json` `proxy` field)
- Build: `npm run build`

The backend reads `DATABASE_URL` from `.env` at the repo root (PostgreSQL via psycopg2). Tables are created automatically at startup via `Base.metadata.create_all` in `main.py` — no migration tool is wired up.

## Architecture

The backend follows a **layered architecture** modeled on a Spring-style Java app (the inline comments in `core/database.py` and `models/product_model.py` make the Java/JPA analogies explicit). Each layer lives in its own top-level package:

```
api/          → FastAPI routers (HTTP layer; depends on services + schemas)
services/     → Business logic (depends on repositories)
repositories/ → SQLAlchemy queries (depends on models)
models/       → SQLAlchemy ORM entities (Base from core.database)
schemas/      → Pydantic request/response models
core/         → Cross-cutting infra: database engine/session, rate limiter
tests/        → pytest, using fastapi.testclient.TestClient(app) from main
```

Dependency direction is strictly top-down through that list. `core/database.py` exposes `Base`, `engine`, and a `get_db()` generator dependency that yields a session and closes it in `finally` — every endpoint takes `db: Session = Depends(get_db)`.

`main.py` is the composition root: it instantiates `FastAPI`, mounts CORS (allows `http://localhost:3000`), includes routers, wires the slowapi `Limiter` from `core/limiter.py` (keyed on remote address, applied per-endpoint via `@limiter.limit(...)`), and registers a custom HTTP middleware that logs and exposes request processing time via the `X-Process-Time` response header.

When adding a new resource, create files in this order: `models/<x>_model.py` → `schemas/<x>_schema.py` → `repositories/<x>_repository.py` → `services/<x>_service.py` → `api/<x>_api.py` (define an `APIRouter` with `prefix` and `tags`), then `app.include_router(...)` in `main.py`.

Note: the current `product` layering has some inconsistencies — `api/product_api.py` calls SQLAlchemy directly for GET-by-id / PUT / DELETE rather than going through the service, and `services/product_service.add_product` signature is `(db, product_request)` while `repositories.add_product` is `(product_request, db)`. Preserve or fix deliberately; don't silently "normalize."
