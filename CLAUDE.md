# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Intelligent Procurement System is an OA-style web application for managing enterprise procurement processes. It includes supplier management, procurement workflows, inventory control, financial accounting, and an integrated AI chat assistant.

Key requirements:
- Left-menu, center-main, right-chat three-column layout
- Backend: Python 3.11+ with FastAPI
- Frontend: Vue 3 with Tailwind CSS 4 (partially implemented)
- Database: PostgreSQL 18
- AI integration: pydantic_ai with optional MCP server extensions
- Support for text-only AI chat with database query capabilities (read-only)

### Functional Modules

Based on requirements document (`企业智能物资采购系统需求汇总.txt`), the system includes:

- **Supplier Management**: Supplier registration, information management, evaluation and selection, supplier collaboration
- **Procurement Management**: Procurement需求 submission, approval workflow, order management, inventory receiving, returns management
- **Inventory Control**: Inventory classification, stock operations, inventory monitoring, inventory alerts
- **Financial Accounting**: Cost management, invoice management, payment processing, fund management
- **Business Analysis**: Procurement data analysis, inventory analysis, financial analysis, decision support
- **Reporting**: Standard and customizable reports for procurement, suppliers, inventory, and finance
- **AI Chat Assistant**: Text-only chat with read-only database query capabilities, extendable via MCP servers

### Current State (as of latest exploration)

| Component | Status | Notes |
|-----------|--------|-------|
| **Backend Structure** | ✅ Complete | FastAPI modular architecture with `app/` organization |
| **Database Models** | ✅ Implemented | User, Role, Permission, Supplier, SupplierProduct, ProcurementRequest models defined |
| **Authentication System** | ✅ Implemented | JWT-based registration, login, token refresh endpoints working |
| **Configuration Management** | ✅ Implemented | pydantic-settings with environment variable loading |
| **Database Engine** | ✅ Configured | Async SQLAlchemy 2.0 with asyncpg driver for PostgreSQL |
| **Docker Configuration** | ✅ Configured | docker-compose for PostgreSQL, pgAdmin, and backend services |
| **API Routes** | ✅ Complete | Auth, User Management, and Supplier Management modules fully implemented; Procurement, Inventory, AI modules have placeholder endpoints (mounted); Finance, Analytics, Reports modules have placeholder routers (not yet mounted) |
| **Business Logic Services** | ❌ Not started | `app/services/` directory exists but empty |
| **Validation Schemas** | ✅ Implemented | User, Role, Permission, Supplier, SupplierProduct, SupplierEvaluation schemas implemented in `app/schemas/` |
| **AI Integration** | ⚠️ Structure only | `app/ai/` directory exists; pydantic_ai agents not implemented |
| **Database Migrations** | ✅ Implemented | Alembic configured with initial migration scripts (`a3206323f0db_initial_tables.py`) |
| **Frontend Structure** | ✅ Partially Implemented | Vue 3 UI components, routing, Pinia stores, API service layer; three-column layout with AI chat sidebar (hidden by default) |
| **Frontend Backend Integration** | ⚠️ Partial | User Management and Supplier Management frontend views connected to backend APIs; other modules pending |
| **Testing** | ❌ Not started | `tests/` directory exists but empty |

**Key Working Components:**
- User registration endpoint (`POST /auth/register`) tested and functional
- JWT token generation and validation
- Role-based permission models (admin, department head, management, employee)
- Async database session management
- CORS middleware configured for development
- Database migration scripts (`a3206323f0db_initial_tables.py`) created and ready
- Frontend three-column layout with Vue 3 components, routing, and Pinia state management
- Frontend API service layer with axios interceptors and auth store
- Vite development server with proxy to backend API
- User Management API with full CRUD operations, role and permission management
- Supplier Management API with CRUD operations, product management, and evaluation system
- Pydantic validation schemas for User, Role, Permission, Supplier models
- Frontend User Management view with search, filtering, and real-time data
- Frontend Supplier Management view with search, filtering, and rating display

**Pending Implementation:**
- Procurement workflow API endpoints (backend)
- Inventory control API endpoints (backend)
- Financial accounting API endpoints (backend)
- Analytics and reporting API endpoints (backend)
- AI chat integration with pydantic_ai (backend)
- Business logic services layer (backend)
- Frontend-backend integration for remaining modules (Procurement, Inventory, Finance, Analytics, AI)
- Test suite (backend and frontend)
- User and Supplier management UI enhancements (create, edit, delete dialogs)

## Development Environment

### Python Backend
- Uses `uv` for package management (see `pyproject.toml` and `uv.lock`)
- Virtual environment: `.venv/` (already in `.gitignore`)
- Python version: 3.11 (specified in `.python-version`)
- Development dependencies: pytest, black, ruff, mypy, pre-commit

### Frontend
- Located in `frontend/` directory with full Vue 3 project structure
- Node.js 22.16+ required (already installed with dependencies)
- Vue 3 with Composition API, Vue Router 4, Pinia for state management
- Tailwind CSS 4 for styling, with Vite as build tool
- API service layer with axios interceptors and proxy configuration to backend
- Three-column layout with AI chat sidebar implemented

### Database
- PostgreSQL 18 required locally or via Docker
- Database migrations using Alembic (configured in `alembic.ini`)
- Docker Compose includes PostgreSQL and pgAdmin services

## Common Commands

### Backend Development
```bash
# Install dependencies
uv sync

# Run development server (FastAPI app is in app/main.py)
uv run uvicorn app.main:app --reload

# Run tests (when implemented)
uv run pytest
# Run single test: uv run pytest path/to/test_file.py::test_function

# Format code with black
uv run black .

# Lint with ruff
uv run ruff check --fix

# Type checking with mypy
uv run mypy .
```

### Frontend Development
```bash
cd frontend

# Install dependencies (package.json exists)
npm install

# Run development server (Vite with proxy to backend on port 5173)
npm run dev

# Build for production
npm run build

# Lint code
npm run lint

# Preview production build
npm run preview
```

Note: The frontend development server runs on http://localhost:5173 with proxy to backend API at http://localhost:8000 (configured in vite.config.js).

### Database Operations
```bash
# Run migrations (initial migration scripts exist)
uv run alembic upgrade head

# Create new migration
uv run alembic revision --autogenerate -m "description"

# Rollback last migration
uv run alembic downgrade -1

# Initialize database with sample data (after migrations)
# Requires psql access to the database
psql -d procurement_db -f scripts/init-db.sql

# Alternative: run initialization via Docker
docker-compose exec postgres psql -U user -d procurement_db -f /docker-entrypoint-initdb.d/init-db.sql
```

### Docker
```bash
# Build and run all services (PostgreSQL, pgAdmin, backend)
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

### Utility Commands
```bash
# Validate Python imports
uv run python test_imports.py

# Test registration endpoint
uv run python test_reg_fix.py

# Create admin user (requires database migrations applied)
uv run python create_admin.py

# Clear Python cache (fix import issues)
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete

# Start backend with Docker only (without frontend)
docker-compose up backend

# Run specific backend module (e.g., auth tests)
uv run pytest app/api/auth/ -v

# Check code coverage (when tests exist)
uv run pytest --cov=app --cov-report=html
```

## Architecture Notes

### High-Level Structure
The system follows a modular monolith architecture with clear separation:

1. **Backend** (`app/`):
   - `api/`: FastAPI routers organized by module (auth, users, suppliers, procurement, inventory, ai, finance, analytics, reports)
   - `core/`: Configuration, security, database engine, dependencies
   - `models/`: SQLAlchemy ORM models (user, role, permission, supplier, supplier_product, etc.)
   - `schemas/`: Pydantic models for request/validation (user, role, permission, supplier models implemented)
   - `services/`: Business logic layer (currently empty)
   - `ai/`: pydantic_ai agent definitions and MCP server integrations (structure exists)
   - `migrations/`: Alembic migration scripts (initial tables migration exists)

2. **Frontend** (`frontend/`):
   - Three-column layout with left navigation, main content, right AI chat sidebar (implemented in `MainLayout.vue`)
   - Views for each module (`DashboardView.vue`, `SuppliersView.vue`, etc.) with placeholder UI
   - Vue Router 4 with route guards and meta titles
   - Pinia stores for state management (auth store with persistence)
   - API service layer (`services/api.js`) with axios interceptors and proxy configuration
   - Vite build tool with Tailwind CSS 4 and PostCSS

3. **Database**:
   - PostgreSQL with tables for users, roles, permissions, suppliers, products, etc.
   - Alembic for migrations

### Key Implementation Details
- **Configuration**: Uses pydantic-settings with environment variable loading (`app/core/config.py`)
- **Authentication**: Full JWT-based auth system (OAuth2 compatible) with registration, login, token refresh, and role-based permissions
- **Database Models**: SQLAlchemy ORM models for users, roles, permissions, suppliers, and supplier products
- **API Structure**: FastAPI routers organized by business domain (auth, users, suppliers, procurement, inventory, ai, finance, analytics, reports)
- **Async Database**: SQLAlchemy 2.0 async engine with asyncpg driver for PostgreSQL
- **Migration Ready**: Alembic configured with initial migration scripts created

### Key Design Patterns
- **Left-Menu-Right-Chat Layout**: Persistent left navigation, main content area, right-side AI chat panel
- **Role-Based Access Control**: Admin, department head, management, employee roles (implemented in models)
- **Modular Design**: Each functional module (suppliers, procurement, inventory, finance) is independently testable
- **AI Integration**: pydantic_ai agents with MCP servers for database query capabilities (read-only)
- **RESTful APIs**: Backend provides JSON APIs for frontend consumption
- **Async Database Operations**: SQLAlchemy 2.0 async API with asyncpg driver

### AI Chat Feature Constraints
- Text-only chat (no file uploads or multimedia)
- Database queries are **read-only** - no insert/update/delete operations
- MCP servers can be extended for custom functionality
- Chat context limited to user's database access permissions

## Development Workflow

1. **Setup**:
   - Install Python 3.11+, Node.js 22.16+, PostgreSQL 18 (or use Docker)
   - Run `uv sync` for backend dependencies
   - Copy `.env.example` to `.env` and configure database connection and AI API key
   - Run `docker-compose up postgres` to start database (or set up local PostgreSQL)

2. **Database**:
   - Ensure PostgreSQL is running (port 5432)
   - Apply existing migrations: `uv run alembic upgrade head`
   - (If model changes) Create new migration: `uv run alembic revision --autogenerate -m "description"`

3. **Running**:
   - Start backend: `uv run uvicorn app.main:app --reload`
   - Start frontend: `cd frontend && npm run dev` (access at `http://localhost:5173`)
   - Access backend API at `http://localhost:8000`
   - API documentation available at `http://localhost:8000/docs` (when debug=True)
   - For Docker: `docker-compose up --build`

4. **Testing**:
   - Backend tests: `uv run pytest` (when tests are implemented)
   - Frontend tests: `cd frontend && npm test` (when implemented)

## Troubleshooting and Known Issues

Based on development progress tracking (`最新开发进度.txt`), the following issues have been encountered and resolved:

### Module Import Conflicts
- **Problem**: Old backup files (`app/api/auth/routes.py.backup`, `app/api/auth/__init__.py.backup`) caused Python module cache to load incorrect UserProfile model definitions.
- **Solution**: Remove or rename backup files outside the module directory, and clear `__pycache__` directories.

### Dependency Injection Function Type Errors
- **Problem**: `require_role` and `require_permission` functions defined as async caused FastAPI dependency injection error: "parameter-less dependency must have a callable dependency".
- **Solution**: Change these functions to synchronous (no `async def`) since they don't contain `await` operations.

### SQLAlchemy Relationship Ambiguity
- **Problem**: User model's `procurement_requests` relationship missing `foreign_keys` parameter, causing `AmbiguousForeignKeysError` with multiple foreign key associations.
- **Solution**: Add `foreign_keys='ProcurementRequest.requester_id'` parameter to the relationship definition.

### Permission Table Query Exceptions
- **Problem**: Registration endpoint failed when querying `user.permissions` due to `role_permission` table permissions issues.
- **Solution**: Add exception handling in registration function to return empty list when permission queries fail.

### API Module Import Errors
- **Problem**: Running `uv run uvicorn app.main:app --reload` returns `AttributeError: module 'app.api.users' has no attribute 'routes'`.
- **Solution**: Ensure `app/api/__init__.py` exports all API modules. Add `from .users import router as users` and include `"users"` in `__all__` list. Also ensure `app/models/__init__.py` exports all model classes used in schemas.

### Current Known Limitations
- Permission system currently returns empty lists; ensure `role_permission` table is properly created and populated with default data.
- Frontend UI components exist but backend integration for procurement, inventory, finance, analytics, and AI modules is pending.
- Business logic services and validation schemas pending implementation.

## Development Tips

### Clearing Python Cache
When encountering module import errors:
```bash
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete
```

### Testing Registration Endpoint
Use the provided test script:
```bash
uv run python test_reg_fix.py
```

### Validating Python Imports
```bash
uv run python test_imports.py
```

### Claude Code Permissions
The `.claude/settings.local.json` allows `curl` and `uv run` commands, enabling Claude Code to execute these operations directly.

### API Testing
- Registration endpoint: `POST /auth/register` (tested and working)
- Login endpoint: `POST /auth/login` (to be tested)
- Token refresh: `POST /auth/refresh` (to be tested)
- User info: `GET /auth/me` (to be tested)

## Configuration Files

- `pyproject.toml`: Python project configuration, dependencies, and build settings
- `uv.lock`: Locked dependencies for reproducible builds
- `.env`: Environment variables (database URLs, API keys, secrets) - **NOT committed**
  - `DATABASE_URL`: PostgreSQL connection string (default: postgresql://user:password@localhost:5432/procurement_db)
  - `SECRET_KEY`: Application secret for JWT/sessions
  - `AI_PROVIDER_API_KEY`: API key for AI service (OpenAI, Anthropic, etc.)
  - `AI_MODEL`: Model identifier (e.g., "gpt-4o-mini")
  - `DEBUG`: Enable debug mode (default: False)
- `alembic.ini`: Database migration configuration with PostgreSQL URL
- `docker-compose.yml`: Multi-service setup for PostgreSQL, pgAdmin, and backend
- `Dockerfile`: Backend Docker image definition using Python 3.11-slim
- `.env.example`: Template for environment variables
- `frontend/vite.config.js`: Vite configuration with proxy to backend
- `frontend/tailwind.config.js`: Tailwind CSS configuration
- `frontend/package.json`: Frontend dependencies and scripts

## Important Notes

- The AI chat feature must **never** allow database modifications
- All database queries through AI must be read-only
- Sensitive data (API keys, database credentials) must be in `.env`
- Database migrations are configured with initial migration scripts created
- Frontend has UI components and service layer but backend integration pending
- Business logic services and validation schemas are pending implementation
- The system uses async SQLAlchemy 2.0 with asyncpg for PostgreSQL
- CORS is configured to allow all origins in development; adjust for production