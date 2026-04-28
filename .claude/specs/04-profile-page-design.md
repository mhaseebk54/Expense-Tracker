# Spec: Profile Page Design

## Overview
This feature implements the user profile page for Spendly. The profile page displays the logged-in user's account information (name, email, member since date) and provides a central hub for accessing expense management features. This page serves as the first authenticated page users see after logging in, and establishes the foundation for the expense tracking dashboard.

## Depends on
- Step 01 — Database Setup (users table must exist)
- Step 02 — Registration (users must be able to register)
- Step 03 — Login and Logout (users must be able to authenticate)

## Routes
- `GET /profile` — Display user profile information — logged-in only
- `GET /dashboard` — Display expense dashboard (redirect to this after login in future steps) — logged-in only

## Database changes
No database changes. The users table already stores name, email, and created_at which are sufficient for the profile page.

## Templates
- **Create:** `templates/profile.html` — Profile page extending `base.html` with user info card, account stats placeholder, and navigation to expense features
- **Modify:** `templates/base.html` — Update navigation to show "Profile" link when user is logged in, and "Logout" button
- **Modify:** `app.py` — Update `/profile` route to fetch and display user data instead of returning placeholder text

## Files to change
- `app.py` — Implement the profile() route to fetch user from database and render profile template
- `templates/base.html` — Add conditional navigation based on login state

## Files to create
- `templates/profile.html` — New profile page template

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw sqlite3 via get_db()
- Parameterised queries only — never use f-strings in SQL
- The profile route must check if user is logged in via `session.get("user_id")`
- If not logged in, redirect to `/login`
- Use `get_user_by_id(user_id)` helper function in database/db.py
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `url_for()` for every internal link — never hardcode paths
- Profile page must display: user name, email, member since date
- Profile page must include cards/links to: Add Expense, View All Expenses (placeholders for future steps)
- Format dates in a human-readable format (e.g., "April 24, 2026")

## Definition of done
- Visiting GET /profile without being logged in redirects to /login
- Visiting GET /profile while logged in displays the user's name, email, and member since date
- The profile page includes visual cards/sections for future expense management features
- The navigation in base.html shows "Profile" link when logged in
- The navigation in base.html shows "Logout" button when logged in
- The navigation shows "Login" and "Register" buttons when NOT logged in
- All links use url_for() for route generation
- The page styling is consistent with the existing landing page design
