# Smart Apartment & Masjid Fund Management System

A Flask-based web application with two modules:
1. **Apartment** — manage apartments, residents, complaints, maintenance, and announcements
2. **Masjid Fund Management** — track donations (no donor names), expenses, and balance

Built for beginners — clean code, simple logic, lots of comments.

---

## Quick Start

```bash
# 1. Clone and enter project
cd appartment

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Tailwind CSS and build styles
npm install && npm run build:css

# 4. Create admin user
python seed_admin.py

# 5. Run
python app.py
```

Login at `http://127.0.0.1:5000/auth/login` with **admin / admin123**.

---

## Project Structure

```
appartment/
├── app.py                  # Flask app factory
├── config.py               # Configuration (DB, secret key)
├── seed_admin.py           # Creates first admin user
├── requirements.txt        # Python dependencies
├── package.json            # Tailwind CSS npm setup
├── tailwind.config.js
├── Dockerfile & docker-compose.yml
│
├── models/
│   ├── user.py             # User model (admin/resident roles)
│   ├── apartment.py        # Apartment, Resident, Complaint, MaintenanceRequest, Announcement
│   └── masjid.py           # Donation, Expense (no donor names)
│
├── routes/
│   ├── auth_routes.py      # Login, Register, Logout, Dashboard
│   ├── apartment_routes.py # Apartment CRUD, residents, complaints, maintenance
│   └── masjid_routes.py    # Donations, expenses, balance
│
├── templates/
│   ├── base.html           # Base layout with sidebar
│   ├── dashboard.html      # Main dashboard with stats
│   ├── login.html / register.html
│   ├── apartment/          # Apartment module templates
│   └── masjid/             # Masjid fund templates
│
├── static/
│   ├── css/input.css       # Tailwind source
│   └── js/main.js
│
└── .github/workflows/ci.yml
```

---

## Modules Explained

### Authentication
- Register users (admin only)
- Login / Logout
- Two roles: **admin** and **resident**
- Protected routes with `@login_required`

### Apartment
| Feature | What it does |
|---|---|
| Add Apartment | Register a unit with owner details |
| Add Resident | Assign a user to an apartment |
| View Apartments | List all units with occupancy |
| Complaints | Log and resolve complaints per unit |
| Maintenance | Track repair requests (pending → in_progress → done) |
| Announcements | Post community notices |

### Masjid Fund Management
- **Donations** — record amount + optional note (NO donor name)
- **Expenses** — record by category (electricity, cleaning, etc.)
- **Dashboard** — shows total donations, total expenses, remaining balance
- Transaction history for both donations and expenses

---

## Docker Usage

```bash
docker compose up --build
```

Opens at `http://localhost:5000`.

---

## CI/CD

On every push, GitHub Actions:
1. Installs Python + dependencies
2. Runs Ruff linter
3. Verifies the Flask app imports and starts correctly

---

## Common Errors

| Error | Fix |
|---|---|
| `pip install` fails with PEP 668 | Use `--break-system-packages` or create a venv |
| `npm run build:css` missing | Run `npm install` first |
| DB tables not found | Delete `instance/app.db` and restart |
| Port 5000 in use | Set `--port 5001` or kill the existing process |

---

## Tech Stack

- **Backend:** Python, Flask, SQLAlchemy, Flask-Login
- **Frontend:** Tailwind CSS, Jinja2, JavaScript
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **DevOps:** Docker, GitHub Actions

---

## Production Deployment

```bash
# Set environment variables
export SECRET_KEY="your-strong-secret-key"
export DATABASE_URL="postgresql://user:password@localhost:5432/apartment_db"
```

| Step | Command |
|---|---|
| Build Tailwind CSS | `npm run build:css` |
| Run with Gunicorn | `gunicorn -w 4 -b 0.0.0.0:8000 run:app` |
| Docker Compose | `docker-compose up -d --build` |
| Create admin user | `python seed_admin.py` |

Login at `http://localhost:8000/auth/login` with **admin / admin123**.
