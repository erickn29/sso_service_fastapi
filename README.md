# SSO (Single Sign-On) Service

A FastAPI-based Single Sign-On authentication service that provides secure user
authentication and token management.

## Features

- User authentication with JWT tokens
- Access and refresh token functionality
- Token verification endpoint
- Admin user management
- Secure password handling with bcrypt
- PostgreSQL database integration
- Redis caching

## Tech Stack

- Python 3.12
- FastAPI framework
- SQLAlchemy (async with asyncpg)
- PostgreSQL
- Redis
- Alembic for migrations
- Poetry for dependency management
- pytest for testing

## Requirements

- Python 3.12+
- PostgreSQL
- Redis

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd sso
```

2. Install dependencies using Poetry:

```bash
poetry install
```

3. Configure environment variables:

Create a `.env` file in the `secrets/` directory with the following variables (customize
as needed):

```
APP__DEBUG=true
APP__SECRET_KEY=your_secret_key

AUTH__ACCESS_TOKEN_EXPIRE=300
AUTH__REFRESH_TOKEN_EXPIRE=1296000

DB__USER=postgres
DB__PASSWORD=postgres
DB__HOST=localhost
DB__PORT=5432
DB__NAME=sso_db

REDIS__HOST=localhost
REDIS__PORT=6379
REDIS__DB=10
```

4. Run database migrations:

```bash
cd src
alembic upgrade head
```

5. Create an admin user:

```bash
python src/create_admin_user.py
```

## Running the Application

Start the application with uvicorn:

```bash
uvicorn src.main:app --reload
```

The API will be available at http://localhost:8000

API documentation is available at:

- Swagger UI: http://localhost:8000/docs/ (only in debug mode)
- ReDoc: http://localhost:8000/redoc/ (only in debug mode)

## API Endpoints

- `[POST] /api/v1/auth/login/` - Get access and refresh tokens
- `[GET] /api/v1/auth/token/` - Refresh access token
- `[POST] /api/v1/auth/token/verify/` - Verify token validity
- `[GET] /api/healthcheck/` - Health check endpoint (admin/service only)
- `[POST] /api/v1/user/` - Add user
- `[GET] /api/v1/user/{user_id}/` - Get user info
- `[PUT] /api/v1/user/{user_id}/` - Update user info
- `[DELETE] /api/v1/user/{user_id}/` - Deactivate user

## Development

### Code Style

The project uses:

- Ruff for linting
- Black for code formatting
- Mypy for static type checking

Run linting:

```bash
ruff check .
```

Run formatting:

```bash
black .
```

### Testing

Run tests:

```bash
pytest
```

## License

[Specify license]