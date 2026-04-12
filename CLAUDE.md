# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask-based expense tracking web application called "Spendly". The application allows users to register, login, and track their expenses with categorization and visualization features.

## Codebase Structure

- `app.py` - Main Flask application with route definitions
- `database/` - Database setup and management (currently placeholders)
- `templates/` - Jinja2 HTML templates for frontend rendering
- `static/` - CSS, JavaScript, and other static assets
- `requirements.txt` - Python dependencies (Flask, Werkzeug, pytest)

## Key Routes

- `/` - Landing page with marketing content
- `/register` - User registration page
- `/login` - User login page
- `/terms` - Terms of service page
- `/privacy` - Privacy policy page
- `/profile` - User profile page (placeholder)
- `/expenses/add` - Add expense form (placeholder)
- `/expenses/<id>/edit` - Edit expense form (placeholder)
- `/expenses/<id>/delete` - Delete expense functionality (placeholder)

## Development Commands

### Running the Application
```bash
python app.py
```
The application runs on http://localhost:5001 in debug mode.

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Running Tests
```bash
pytest
```

## Architecture Notes

1. **Frontend**: Uses Jinja2 templating with a base template (`base.html`) that includes consistent navigation and footer. Styling is handled with custom CSS in `static/css/style.css`.

2. **Backend**: Flask application with placeholder routes that need implementation. Database functionality is planned but not yet implemented.

3. **Database**: Currently has placeholder files (`database/db.py`) that need to be implemented with SQLite connection management and table creation.

4. **Testing**: Pytest is included as a dependency but no test files exist yet.

## Implementation Status

Several routes are currently implemented as placeholders with messages indicating they will be completed in future steps:
- Logout functionality
- Profile page
- Add/edit/delete expense functionality

## Common Development Tasks

When implementing new features, focus on:
1. Completing the database implementation in `database/db.py`
2. Implementing the placeholder routes in `app.py`
3. Adding corresponding templates in the `templates/` directory
4. Following the existing CSS styling patterns in `static/css/style.css`