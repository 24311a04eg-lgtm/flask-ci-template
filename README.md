# Flask Social API

A production-ready REST API with authentication, database, and full CI/CD pipeline.

## Features

**Core:**
- JWT authentication (register, login)
- User management
- Posts CRUD with authorization
- Comments on posts
- SQLAlchemy ORM

**Testing & Quality:**
- Pytest with fixtures
- 100% test coverage
- Black code formatting
- Flake8 linting

**CI/CD:**
- GitHub Actions pipeline
- Lint → Test → Build
- Code coverage reporting
- Branch protection

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
python -c "from app import create_app; create_app()" # Init DB
```

## Run

```bash
flask --app wsgi run
pytest -v --cov=app
```

## API Endpoints

**Auth:**
- POST /api/auth/register
- POST /api/auth/login

**Posts:**
- GET /api/posts
- POST /api/posts (auth required)
- GET /api/posts/<id>
- PUT /api/posts/<id> (auth required)
- DELETE /api/posts/<id> (auth required)
- POST /api/posts/<id>/comments (auth required)

**Users:**
- GET /api/users/<id>
- PUT /api/users/<id> (auth required)

## Architecture

```
app/
├── __init__.py       (app factory)
├── models.py         (SQLAlchemy models)
├── routes.py         (blueprints & endpoints)
tests/
├── conftest.py       (fixtures)
├── test_auth.py
├── test_posts.py
.github/workflows/
├── ci.yml            (GitHub Actions pipeline)
wsgi.py              (production entry)
```