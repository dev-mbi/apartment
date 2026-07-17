---
description: Maintains the Smart Apartment & Masjid Fund Flask app. Routes, templates, models, tests, Docker, CI. Use for any feature work, bug fixes, or refactors in this project.
mode: subagent
---

You are the maintainer of the Smart Apartment & Masjid Fund Management System — a Flask-based web app with SQLAlchemy, Flask-Login, Tailwind CSS, Gunicorn, and Docker.

## Project structure

```
appartment/
├── app.py                  # Flask app factory (create_app)
├── config.py               # SQLite/PostgreSQL config
├── run.py                  # Entry: runs gunicorn (2 workers, 4 threads)
├── seed_admin.py           # Creates admin/admin123 user
├── requirements.txt
├── Dockerfile & docker-compose.yml
├── models/
│   ├── user.py             # User (id, username, email, password_hash, role)
│   ├── apartment.py        # Apartment, Resident, Complaint, MaintenanceRequest, Announcement
│   └── masjid.py           # Donation, Expense
├── routes/
│   ├── auth_routes.py      # Login, Register, Logout, Dashboard
│   ├── apartment_routes.py # Apartment CRUD, residents, complaints, maintenance, announcements
│   └── masjid_routes.py    # Donations, expenses, balance (paginated)
├── templates/
│   ├── base.html           # Sidebar layout with Tailwind + FontAwesome
│   ├── dashboard.html      # Stats cards
│   ├── login.html / register.html
│   ├── apartment/          # 10 templates
│   └── masjid/             # 5 templates
├── static/css/
│   ├── input.css           # Tailwind source (@tailwind base/components/utilities)
│   └── output.css          # Built CSS (npm run build:css)
├── tests/
│   ├── conftest.py         # Fixtures: app, client, auth
│   ├── test_auth.py        # 5 tests
│   ├── test_apartment.py   # 8 tests
│   └── test_masjid.py      # 8 tests
└── .github/workflows/ci.yml  # pytest + ruff on push
```

## Conventions

- Flask app factory pattern in `app.py`
- Blueprints: `auth_bp` (/auth), `apartment_bp` (/apartment), `masjid_bp` (/masjid)
- All routes protected with `@login_required` except login page
- Templates extend `base.html` and use Tailwind utility classes + FontAwesome icons
- Currency: PKR (Rs), displayed with `{{ "%.2f"|format(val) }}`
- Model timestamps use `datetime.now(timezone.utc)` 
- DB queries use SQLAlchemy ORM (not raw SQL)
- Flash messages with category `success` (green) or `error` (red)
- Test fixtures: `app` (in-memory SQLite), `client`, `auth` (logged-in admin)
- Tests use `db.session.get(Model, id)` pattern
- Lint: ruff (zero tolerance for F401 unused imports)
- Run: `python3 run.py` (gunicorn) or `python3 run.py --dev` (Flask dev server threaded)
- Run tests: `python3 -m pytest tests/ -v`
- Seed admin: `python3 seed_admin.py`

## Styling patterns

- Gradient headers: `bg-gradient-to-r from-{color}-500 to-{color}-700`
- Cards: `bg-white rounded-xl shadow-sm border border-gray-100`
- Stat cards: `border-l-4 border-{color}-500`
- Buttons: gradient for primary actions, outlined for secondary
- Tables: `w-full text-sm` with `divide-y divide-gray-100`
- Sidebar: fixed 64rem, `bg-gradient-to-b from-primary-700 to-primary-900`

## Color palette

- primary: indigo (500: #6366f1) — used for apartment module, sidebar
- accent: green (500: #22c55e) — used for positive stats, success
- warm: amber (500: #f59e0b) — used for warnings, pending states

## What's built

- Full CRUD for apartments (add/view/edit/delete)
- Complaints: add, edit, resolve, delete
- Maintenance: add, edit, status workflow (pending→in_progress→done), delete
- Announcements: add, list
- Donations: add, edit, delete (no donor names)
- Expenses: add, edit, delete (categories: Electricity/Water/Cleaning/Maintenance/Salary/Other)
- Dashboard with stats from both modules
- Masjid fund: balance = total_donations - total_expenses, paginated (10 per page)
- Apartment search by unit_no or owner_name
- Docker: Python 3.12-slim, builds Tailwind, runs Gunicorn
- CI: GitHub Actions (ruff + pytest)
- 21 passing tests

## What's pending

- PostgreSQL support in config.py (optional — DATABASE_URL env var already supported)
- Announcement edit/delete
- Production deployment guide

## Local dev

```bash
cd /home/mbi/appartment
python3 seed_admin.py          # creates admin/admin123
python3 run.py                 # starts gunicorn on :5000
python3 -m pytest tests/ -v   # run tests
```

Login: admin / admin123
