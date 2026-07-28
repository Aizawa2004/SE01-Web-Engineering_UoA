# The Blogs

Shared blog platform project using Django + HTMX.

## Current Development Phase

This repository is currently in specification and AI-tooling hardening phase.

In scope now:

- Requirements and architecture hardening
- Agent and skill tuning
- Development workflow documentation

Out of scope now:

- Django scaffolding creation
- Application code implementation
- Database migration execution

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
