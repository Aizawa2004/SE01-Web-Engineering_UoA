# Project Context: The Blogs (Django + HTMX)

## 1. Product Summary
The Blogs is a shared blog platform where registered users can publish posts and browse posts with fast filtering UX.

## 2. Core User Scenarios
- Register with unique username and password.
- Create and publish a post.
- Browse all posts in reverse chronological order.
- Filter posts by author.
- Filter posts by date with a calendar UI.
- Search posts by title keyword (optional feature, but planned from initial architecture).

## 3. Data Model Baseline
- Users: id, username, password (Django auth based).
- Posts: id, title, content, created_at, author (FK to Users).

Implementation notes:
- Ordering: newest first by default.
- Query-focused indexes should be prepared for fields used by filtering and sorting.

## 4. URL Design (Implementation Policy)
Primary list screen should remain a single source of truth and be query-driven.

| Purpose | Method | Path | Name | Notes |
|---|---|---|---|---|
| Home / Post list | GET | / | posts:list | Supports query params below |
| Post list alias | GET | /posts/ | posts:list | Same behavior as home |
| Create post | GET, POST | /posts/new/ | posts:create | Auth required |
| Register | GET, POST | /accounts/register/ | accounts:register | Public |
| Login | GET, POST | /accounts/login/ | accounts:login | Public |
| Logout | POST | /accounts/logout/ | accounts:logout | CSRF required |

Canonical query parameters for list screen:
- author: username string
- date: YYYY-MM-DD
- q: title search keyword
- page: pagination page number

Guideline:
- Author link and calendar selection should navigate by query params, not by isolated business logic endpoints.
- HTMX requests should return partial HTML while preserving equivalent full-page rendering for non-HTMX access.

## 5. Template Split Strategy (Django + HTMX)
Recommended template structure:

- templates/base.html
- templates/posts/list_page.html
- templates/posts/partials/post_list.html
- templates/posts/partials/filter_bar.html
- templates/posts/partials/pagination.html
- templates/posts/create.html
- templates/accounts/register.html
- templates/accounts/login.html

Rendering policy:
- Full request: render list_page.html.
- HTMX request: render only the minimal partial target (typically post_list + pagination region).
- Keep UI state in URL query so refresh/share/back-forward maintains identical view state.

## 6. Security Requirements
Mandatory requirements for all implementation phases:

- Use Django ORM exclusively for data access paths handling user input.
- Include CSRF token in all HTML forms and HTMX POST requests.
- Restrict write actions (create/edit/delete) to authenticated users.
- Escape all user-generated output with Django auto-escape defaults; do not mark unsafe HTML as safe.
- Validate and normalize query parameters (author, date, q, page).
- Use POST for logout to avoid CSRF-prone GET logout behavior.
- Keep secrets in environment variables, never hardcode in source.

## 7. Performance and Query Guidelines
- Use select_related("author") for post list to avoid N+1 author lookup.
- Add indexes for fields used frequently:
	- created_at
	- title (if title search is used)
	- author + created_at composite index
- Paginate aggressively to keep list rendering stable.

## 8. Acceptance Criteria (DoD)
### 8.1 Register and Write
- User can register and then create a post while authenticated.
- Unauthenticated access to create page is blocked or redirected.

### 8.2 Display All Posts
- List is sorted by newest first.
- Pagination controls for next/previous are visible when needed.

### 8.3 Filter by Author
- Clicking author updates list to only that author's posts.
- URL reflects author query parameter.

### 8.4 Filter by Calendar Date
- Date selection updates list to posts from selected day only.
- URL reflects date query parameter.

### 8.5 Search by Title (Optional)
- Entered keyword filters title by partial match.
- Search state survives page reload through URL query.

### 8.6 HTMX Behavior
- Filter/pagination interactions work without full page reload via HTMX.
- Same actions remain functional without JavaScript (full-page fallback).

### 8.7 Quality Gate
- Lint passes (Ruff).
- Tests for list ordering, filter, search, and pagination pass.
- No security rule violations listed in Section 6.

## 9. Current Phase Scope Control
Current project phase is Exercise 6: writing basic view functions and URL routing.

Completed in this phase:
- Django project initialized at repository root.
- blog app created and added to INSTALLED_APPS.
- Post model implemented (author, title, content, created_at, __str__).
- Post model registered in Django admin.
- Initial migrations generated and applied to SQLite database.
- Basic model unit tests added and passing.
- Basic view functions implemented for list, author filter, date filter, and dummy create flows.
- URL routing connected from config.urls to blog.urls.
- View-level tests added and passing.

Out of scope for this phase:
- HTML template rendering
- HTMX interaction wiring
- End-to-end UI implementation

## 10. Tech Stack
- Python 3.11+
- Django 5.x
- HTMX
- uv package manager
- Ruff and Coverage for quality control

## 11. Exercise 5 Deliverables
- Django project scaffold files: manage.py, config/*
- App scaffold files: blog/*
- Initial schema migration: blog/migrations/0001_initial.py
- Local database file: db.sqlite3
- Model tests: blog/tests.py

## 12. Exercise 6 View API Summary
- GET / -> post-list: returns all posts as plain text lines in "title by author" format.
- GET /author/<username>/ -> post-list-by-author: returns only posts for the given username.
- GET /date/<YYYY-MM-DD>/ -> post-list-by-date: returns only posts whose created_at date matches the path date.
- GET /post/new/ -> post-create-dummy: creates a fixed dummy post and redirects to post-list.
