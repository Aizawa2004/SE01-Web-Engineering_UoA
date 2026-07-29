# render.com

**[The Blog](https://theblog-se01-web-engineering-uoa.onrender.com)**
**Click on the URL to see this project in action.**

# The Blog

A shared blog platform web application built using Django + HTMX, managed via the `uv` package manager.

## Product Goals & Features

* **User Authentication**: Secure registration, login, and logout capabilities.
* **CRUD Operations**: Authenticated users can create, read, update, and delete blog posts and comments.
* **Dynamic Filtering & Search**:
* Filter posts by author.
* Filter posts by date.
* Search posts by title keyword.


* **Asynchronous UX (HTMX)**: Incremental search and dynamic list updates without full-page reloads, with full-page fallbacks.
* **Pagination**: Smooth navigation with previous/next controls.

## Environment & Tech Stack

* **Python**: 3.11+
* **Package Manager**: `uv`
* **Framework**: Django 5.2+
* **Frontend / Async**: HTMX (`django-htmx`)
* **Production Server**: Waitress
* **Static File Serving**: WhiteNoise
* **Quality & Testing Tools**: Ruff (Linting), Coverage (`coverage.py`), Django Test Suite (31 tests passing)

## Local Setup & Quickstart

1. Clone the repository and enter the directory:
```bash
git clone <your-github-repo-url>
cd TheBlog
```


2. Create and activate the virtual environment using `uv`:
```bash
uv venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
uv sync
```


4. Run database migrations:
```bash
uv run python manage.py migrate
```

5. Start the development server:
```bash
uv run python manage.py runserver
```


6. Open `[http://127.0.0.1:8000/](http://127.0.0.1:8000/)` in your browser.

## Development & Quality Commands

To maintain code quality and verify functionality, use the following commands:

```bash
# Run static code analysis (Linter)
uv run ruff check .

# Run the complete test suite (31 tests)
uv run python manage.py test

# Run tests with coverage measurement
uv run coverage run --source='.' manage.py test
uv run coverage report
```

## HTMX Strategy & Implementation

* **URL-Query Driven**: List rendering and filtering state are tied to URL query parameters (`q`, `author`, `date`, `page`).
* **Partial Responses**: The views check `request.htmx` to return partial HTML templates (`post_list_content.html`) for asynchronous updates, while returning the full page (`post_list.html`) for normal requests.
* **URL History Push**: `hx-push-url="true"` is utilized on dynamic interactions to ensure browser history, back/forward navigation, and bookmarks function correctly.

## Security Measures

* **ORM Protection**: Uses Django ORM to protect against SQL injection.
* **CSRF Protection**: Comprehensive CSRF token integration across forms and HTMX requests.
* **Authentication Guards**: Write actions (creating/deleting posts) are protected by login required decorators/mixins.
* **Method Restrictions**: Logout is strictly restricted to `POST` requests to prevent cross-site request forgery.
* **Environment Isolation**: Secrets and host configs are strictly handled via environment variables.

## Deployment Guide

### Local Production Simulation

To test the production behavior locally:

1. Install dependencies:
```bash
uv sync
```

2. Collect static files for WhiteNoise:
```bash
uv run python manage.py collectstatic --noinput
```

3. Run database migrations:
```bash
uv run python manage.py migrate
```

4. Start the production WSGI server (Waitress):
```bash
waitress-serve --port=8000 config.wsgi:application
```



### External Hosting (Render.com)

1. Push your repository to GitHub.
2. Create a new Web Service on Render and connect your repository.
3. Configure settings:
* **Runtime**: Python 3
* **Build Command**:
```bash
uv sync && uv run python manage.py collectstatic --noinput && uv run python manage.py migrate
```

* **Start Command**:
```bash
waitress-serve --port=$PORT config.wsgi:application
```


4. Set required Environment Variables on Render:
* `DEBUG` = `False`
* `SECRET_KEY` = `<strong-random-secret>`
* `ALLOWED_HOSTS` = `theblog-se01-web-engineering-uoa.onrender.com`
* `CSRF_TRUSTED_ORIGINS` = `[https://theblog-se01-web-engineering-uoa.onrender.com](https://theblog-se01-web-engineering-uoa.onrender.com)`
