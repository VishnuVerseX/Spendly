# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

"Spendly" — a personal expense tracker built as a learning project with Flask, server-rendered Jinja templates, and vanilla JS/CSS (no frontend framework, no build step). The app is intentionally incomplete: routes and modules exist as scaffolding with comments marking what students implement at each step.

## Running the app

```bash
pip install -r requirements.txt
python app.py
```

Runs on `http://localhost:5001` with debug mode on.

## Testing

`pytest` and `pytest-flask` are listed in `requirements.txt`, but no test files exist yet. Run tests with:

```bash
pytest
```

## Architecture

- `app.py` — all Flask routes live here directly (no blueprints). Implemented routes (`/`, `/register`, `/login`, `/terms`, `/privacy`) just render templates. Placeholder routes (`/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`) currently return plain strings and are meant to be built out — check the comment above each before assuming behavior.
- `database/db.py` — intended to hold `get_db()` (SQLite connection, row_factory + foreign keys enabled), `init_db()` (CREATE TABLE IF NOT EXISTS), and `seed_db()`. Not yet implemented — no SQLite integration exists in the app currently despite `expense_tracker.db` being gitignored in anticipation of it.
- `templates/base.html` — shared layout (nav, footer, font/CSS links) that other templates extend via `{% extends "base.html" %}` and `{% block content %}`. Match this pattern for new pages rather than duplicating the `<head>`/nav/footer.
- `static/css/style.css` — single stylesheet for the whole site (~660 lines); no per-page CSS files despite what old task notes (`file.txt`) mention (a referenced `landing.css` does not exist — everything lives in `style.css`).
- `static/js/main.js` — single JS file for the whole site, vanilla JS only (no framework, no dependencies) per project convention.

## Conventions to follow

- No JS framework and no CSS/JS build pipeline — write plain JS and plain CSS directly into `main.js` / `style.css`.
- New pages should extend `templates/base.html` and match the existing visual style (fonts: DM Serif Display + DM Sans, loaded via Google Fonts in `base.html`).
- When a task only asks to change one section of a page (e.g. the hero section), don't touch unrelated markup/CSS in the same file.
