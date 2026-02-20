# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Intelligent Procurement System is an OA-style web application for managing enterprise procurement processes. It includes supplier management, procurement workflows, inventory control, financial accounting, and an integrated AI chat assistant.

**Key Technology Stack:**
- Backend: Python 3.11+ with FastAPI, SQLAlchemy 2.0, Alembic
- Frontend: Vue 3 with Tailwind CSS 4, Vite, Pinia
- Database: PostgreSQL 18 (async via asyncpg)
- AI: pydantic_ai with read-only database query capabilities
- Package Management: uv (Python), npm (Node.js)
- Deployment: Docker Compose with PostgreSQL, pgAdmin, backend

**Critical Architecture Constraints:**
- Three-column layout: left navigation, main content, right AI chat sidebar
- AI chat is text-only with **read-only** database access (no modifications)
- JWT-based authentication with role-based permissions (admin, manager, employee)
- Async SQLAlchemy 2.0 for all database operations

## Current Implementation Status

### Backend (app/)
| Component | Status | Key Notes |
|-----------|--------|-----------|
| **API Structure** | ✅ Complete | Modular FastAPI routers in `app/api/` |
| **Authentication** | ✅ Working | JWT registration, login, token refresh |
| **User Management** | ✅ Complete | Full CRUD, role/permission management, statistics |
| **Supplier Management** | ✅ Complete | Supplier CRUD, products, evaluations |
| **Database Models** | ✅ Implemented | User, Role, Permission, Supplier, SupplierProduct, ProcurementRequest |
| **Migrations** | ✅ Configured | Alembic with `a3206323f0db_initial_tables.py` (active migration) |
| **Configuration** | ✅ Working | pydantic-settings with `.env` loading |
| **Procurement API** | ⚠️ Placeholders | Basic endpoints return placeholder messages |
| **Inventory API** | ⚠️ Placeholders | Basic endpoints return placeholder messages |
| **AI Integration** | ⚠️ Structure only | `app/ai/` directory exists, agents not implemented |
| **Business Logic** | ❌ Not started | `app/services/` directory empty |
| **Finance/Analytics/Reports** | ❌ Routers not mounted | Routers exist but not mounted in `app/main.py` |

### Frontend (frontend/)
| Component | Status | Key Notes |
|-----------|--------|-----------|
| **Three-Column Layout** | ✅ Implemented | `MainLayout.vue` with left-nav, main, right-chat |
| **Vue 3 Structure** | ✅ Complete | Vue Router 4, Pinia stores, Vite build |
| **API Service Layer** | ✅ Complete | Axios interceptors, proxy to backend (`localhost:8000`) |
| **User Management UI** | ✅ Connected | Full integration with `/api/users/*` endpoints |
| **Supplier Management UI** | ✅ Connected | Integration with `/api/suppliers/*` endpoints |
| **Other Module UIs** | ⚠️ Placeholders | Views exist but backend integration pending |

**Active Migration:** `a3206323f0db_initial_tables.py` (ignore `b01260bc56af_initial.py`)

## Critical Development Commands

### Environment Setup
```bash
# Backend dependencies (uses uv)
uv sync

# Frontend dependencies
cd frontend && npm install

# Database setup (Docker)
docker-compose up postgres -d
uv run alembic upgrade head
```

### Development Servers
```bash
# Backend (port 8000) - FastAPI with auto-reload
uv run uvicorn app.main:app --reload

# Frontend (port 5173) - Vite with proxy to backend
cd frontend && npm run dev
```
**Access:** Frontend: http://localhost:5173 | Backend API: http://localhost:8000 | Docs: http://localhost:8000/docs (when DEBUG=True)

### Database Operations
```bash
# Apply migrations
uv run alembic upgrade head

# Create new migration (after model changes)
uv run alembic revision --autogenerate -m "description"

# Rollback last migration
uv run alembic downgrade -1

# Initialize with sample data (requires psql)
psql -d procurement_db -f scripts/init-db.sql
```

### Code Quality
```bash
# Format Python code
uv run black .

# Lint with auto-fix
uv run ruff check --fix

# Type checking
uv run mypy .
```

### Testing & Validation
```bash
# Test imports (validate module structure)
uv run python test_imports.py

# Test registration endpoint
uv run python test_reg_fix.py

# Create admin user (after migrations)
uv run python create_admin.py
```

### Docker Operations
```bash
# Full stack (PostgreSQL, pgAdmin, backend)
docker-compose up --build

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Start only backend (requires running PostgreSQL)
docker-compose up backend
```

## Architecture Patterns

### Backend Structure (`app/`)
- **API Modules**: Single-file routers in `app/api/` (e.g., `users.py`, `suppliers.py`)
- **Dependency Injection**: Synchronous functions (`get_current_user`, `require_role`, `require_permission`) - **must be sync** (not async) due to FastAPI constraints
- **Database**: Async SQLAlchemy 2.0 with asyncpg driver, session via `get_db()` dependency
- **Configuration**: Centralized in `app/core/config.py` using pydantic-settings
- **Validation**: Pydantic schemas in `app/schemas/` for request/response validation

### Frontend Structure (`frontend/`)
- **Layout**: Three-column design in `src/layouts/MainLayout.vue`
- **State Management**: Pinia stores with `pinia-plugin-persistedstate`
- **API Layer**: `src/services/api.js` with axios interceptors for auth tokens
- **Routing**: Vue Router 4 with route guards and meta titles
- **Build**: Vite with proxy configuration (`/api/*` → `localhost:8000`)

### Database Models
- **User**: Roles (admin, manager, employee), permissions via role_permission table
- **Supplier**: Basic info, products, evaluations, ratings
- **ProcurementRequest**: Requester, approver, status workflow
- **Relationships**: User ↔ Role (many-to-many), Role ↔ Permission (many-to-many)

## Known Issues & Solutions

### Database Configuration Inconsistency
**Problem**: Four different database configurations exist:
1. `.env`: `postgresql://postgres:123456@localhost:5432/intelligentProcurementSystem`
2. `app/core/config.py`: `postgresql://user:password@localhost:5432/procurement_db`
3. `alembic.ini`: `postgresql://user:password@localhost:5432/procurement_db`
4. `docker-compose.yml`: `postgresql://procurement_user:procurement_password@postgres:5432/procurement_db`

**Solution**: Update all configurations to match `.env` or create consistent configuration.

### Module Import Conflicts
**Cause**: Backup files (`*.backup`) in `app/api/auth/` cause Python cache issues.
**Solution**: Remove backup files from module directories and clear `__pycache__`:
```bash
# Windows
rmdir /s /q __pycache__ 2>nul
del /s /q *.pyc 2>nul

# Unix/Linux/macOS
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete
```

### Permission System Issues
**Problem**: Registration endpoint fails when querying `user.permissions` due to `role_permission` table issues.
**Workaround**: Exception handling returns empty permission list. Ensure `role_permission` table is properly populated.

### API Module Import Errors
**Problem**: `AttributeError: module 'app.api.users' has no attribute 'routes'`
**Solution**: Ensure `app/api/__init__.py` exports all routers and `app/models/__init__.py` exports all models.

## Development Workflow

1. **Start Database**: `docker-compose up postgres -d` (or local PostgreSQL on port 5432)
2. **Apply Migrations**: `uv run alembic upgrade head`
3. **Start Backend**: `uv run uvicorn app.main:app --reload` (port 8000)
4. **Start Frontend**: `cd frontend && npm run dev` (port 5173)
5. **Test API**: Use `test_reg_fix.py` or access `http://localhost:8000/docs`

## Configuration Files Reference

- **`.env`**: Environment variables (database, secrets, AI keys) - **NOT committed**
- **`pyproject.toml`**: Python dependencies and project config
- **`alembic.ini`**: Database migration configuration
- **`docker-compose.yml`**: Multi-service Docker setup
- **`frontend/vite.config.js`**: Vite proxy config (`/api/*` → `localhost:8000`)
- **`frontend/tailwind.config.js`**: Tailwind CSS configuration
- **`.claude/settings.local.json`**: Claude Code permissions (allows `curl` and `uv run`)

## Important Notes

1. **AI Security**: AI chat must **never** allow database modifications (read-only queries only)
2. **Migration Management**: Always use `a3206323f0db_initial_tables.py` as the active migration
3. **Frontend Proxy**: Frontend dev server proxies API calls via Vite configuration
4. **Role-Based Access**: Four system roles: admin, department head, management, employee
5. **Async Database**: All database operations use SQLAlchemy 2.0 async API
6. **Pending Integration**: Procurement, Inventory, Finance, Analytics, AI modules need backend-frontend integration
7. **Business Logic**: `app/services/` directory is empty - business logic layer pending implementation