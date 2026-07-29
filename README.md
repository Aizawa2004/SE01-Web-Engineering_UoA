# render.com
**[The Blog](https://theblog-se01-web-engineering-uoa.onrender.com)
Click on the URL to see this project in action.**

# The Blogs

Shared blog platform project using Django + HTMX.

## Product Goals

- Users can register and create posts.
- Posts are listed in reverse chronological order.
- Users can filter by author.
- Users can filter by date.
- Users can search by title keyword.
- Pagination works with clear previous/next navigation.

See the detailed implementation policy in [AGENTS.md](AGENTS.md).

## Environment

- Python: 3.11+
- Package manager: uv
- Framework: Django 5.x (already added as dependency)
- Quality tools: Ruff, Coverage

## Local Setup (macOS / Linux)

1. Clone and enter repository.
2. Create virtual environment.
3. Activate virtual environment.
4. Install dependencies.

```bash
git clone <your-github-repo-url>
cd the-blogs
uv venv
source .venv/bin/activate
uv sync
```

## Development Commands

Commands available now (no Django scaffold required):

```bash
# Lint check
uv run ruff check .

# Optional auto-fix
uv run ruff check . --fix

# Format (if you choose to use Ruff formatter)
uv run ruff format .
```

Planned commands for Day 1+ (after Django project is created):

```bash
# Run development server
uv run python manage.py runserver

# Create and apply migrations
uv run python manage.py makemigrations
uv run python manage.py migrate

# Run tests
uv run python manage.py test
```

## Testing Strategy (Planned)

The first implementation milestone should include test coverage for:

- Post ordering (newest first)
- Author filter
- Date filter
- Title keyword search
- Pagination behavior
- Authentication guard for write actions

Coverage policy can be tightened after test suite lands.

## HTMX Strategy

- Keep list rendering URL-query driven.
- Use partial template responses for HTMX requests.
- Preserve full-page fallback for non-JS clients.

Recommended list query keys:

- author
- date
- q
- page

## Security Checklist

- Use Django ORM for user-driven queries.
- Include CSRF token for all forms and HTMX POSTs.
- Keep logout as POST.
- Validate query params before applying filters.
- Keep secrets in environment variables.

## AI Workflow Notes

This repository includes skill definitions under [.agents/skills](.agents/skills) and project rules in [AGENTS.md](AGENTS.md).

Recommended usage:

1. Confirm scope in AGENTS before code generation.
2. Use Django-related skills for model/view/template decisions.
3. Validate output against URL policy, template split policy, and security requirements.

## Deployment Guide

### Local Production Simulation

Use these steps to run the app locally in a production-like mode.

1. Install dependencies.

```bash
uv sync
```

2. Collect static files for WhiteNoise.

```bash
uv run python manage.py collectstatic --noinput
```

3. Apply database migrations.

```bash
uv run python manage.py migrate
```

4. Start the production WSGI server (Waitress).

```bash
uv run waitress-serve --port=8000 config.wsgi:application
```

5. Open the app at http://127.0.0.1:8000

Recommended environment variables for local production simulation:

```bash
export DEBUG=False
export SECRET_KEY="replace-with-a-strong-secret"
export ALLOWED_HOSTS="127.0.0.1,localhost"
```

Optional database variables (non-SQLite setups):

```bash
export DB_ENGINE="django.db.backends.postgresql"
export DB_NAME="your_db_name"
export DB_USER="your_db_user"
export DB_PASSWORD="your_db_password"
export DB_HOST="your_db_host"
export DB_PORT="5432"
```

### External Hosting (Render.com)

1. Push your repository to GitHub.
2. In Render, click New + and choose Web Service.
3. Connect your GitHub repository and select this project.
4. Configure Render service settings:
	- Runtime: Python 3
	- Build Command:

```bash
uv sync && uv run python manage.py collectstatic --noinput && uv run python manage.py migrate
```

	- Start Command:

```bash
waitress-serve --port=$PORT config.wsgi:application
```

5. Set environment variables in Render:
	- DEBUG=False
	- SECRET_KEY=<strong-random-secret>
	- ALLOWED_HOSTS=<your-render-domain>
	- DB_ENGINE, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT (if using external DB)

Notes:
- Render may also use equivalent commands with pip/venv if your runtime is not uv-based.
- Always keep DEBUG=False in production.
- After deploy, verify static assets load correctly and basic pages respond as expected.
