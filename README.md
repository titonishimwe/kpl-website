# Kigali Public Library (KPL) - Django Web Platform

## Description
The official web platform for **Kigali Public Library (KPL)**, built using **Django 6**, **Bootstrap 5**, HTML5, CSS3, and modern JavaScript. The platform serves as a national gateway to educational, cultural, and informational resources across Rwanda, providing digital catalogue integration, space and room bookings, membership card applications, and event announcements.

Developed strictly following the **Django Project Standard Workflow & Initialization Guide**.

---

## Technologies
- **Backend**: Python 3.14 / 3.12, Django 6.1.2
- **Database**: SQLite (Development) / PostgreSQL compatible
- **Frontend**: Bootstrap 5.3.3, Bootstrap Icons, HTML5, CSS3, JavaScript (ES6)
- **Typography & Assets**: DIN Pro custom typography, SVG icons, and responsive imagery
- **Configuration & Security**: `python-dotenv`, CSRF protection, secure cookies, defense-in-depth architecture
- **Image Handling**: Pillow 13.0

---

## Features
- **Real-Time Kigali Library Status**: Live indicator calculating if KPL is currently open or closed with daily operating hours in `Africa/Kigali` timezone.
- **Koha OPAC Catalogue Search**: Direct search integration with the library's Koha Online Public Access Catalog.
- **Membership Application System**:
  - Full online application form with plan selection (Children, Student, Adult, Internet Café).
  - Dynamic parent/guardian verification for junior members under 18.
  - Supporting document uploads (National ID / Passport / Student ID).
  - Integrated payment instructions (MoMo Pay `*182*8*1*021216#` and Card).
  - Stored in database and managed through Django Admin.
- **Room & Space Reservations**:
  - Meeting Rooms (Small, Medium, Large)
  - Discussion Rooms (Grey, Blue, Red) with half-day and full-day rate tracking
  - Event Space booking
  - Online booking request form with email notifications and admin management.
- **Events & Programs**:
  - Event highlights, author talks, storytime, and book club sessions.
  - Interactive event carousel and upcoming schedule.
- **New Arrivals Showcase**:
  - Tabbed book carousel for Adult, Teens, and Children collections.
- **User Authentication & Profile Management**:
  - User registration, login, logout, profile editing, and library card binding.
  - Automatic profile creation via Django signals.
  - Role separation between visitors, staff, and superusers.
- **Interactive Cookie Consent**:
  - Privacy and cookie consent banner storing user choices in `localStorage`.
- **Security & Error Handling**:
  - Custom branded 404, 403, and 500 error pages avoiding technical information leaks.
  - Secure `.env` handling and settings isolation.

---

## Project Structure
```text
kpl-website-main/
├── apps/
│   ├── core/                  # Core library features (Home, About, Spaces, Membership, Events)
│   │   ├── migrations/
│   │   ├── templates/core/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── context_processors.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   └── accounts/              # User authentication, profiles, signals, commands
│       ├── management/commands/create_default_admin.py
│       ├── migrations/
│       ├── templates/accounts/
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py
│       ├── models.py
│       ├── signals.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── config/                    # Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   ├── images/
│   └── fonts/
├── templates/                 # Global templates
│   ├── base.html
│   ├── 404.html
│   ├── 403.html
│   ├── 500.html
│   └── includes/
│       ├── navbar.html
│       ├── footer.html
│       └── messages.html
├── media/                     # Uploaded documents and photos
├── staticfiles/               # Production collected static files
├── .env                       # Environment variables (excluded from git)
├── .env.example               # Example environment template
├── .gitattributes
├── .gitignore
├── .python-version            # Python version used on Render
├── build.sh                   # Render build: install, collectstatic, migrate
├── manage.py
├── render.yaml                # Render Blueprint (web service + Postgres)
├── requirements.txt
└── README.md
```

---

## Installation & Setup

### 1. Clone & Enter Directory
```bash
cd kpl-website-main
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and adjust if needed:
```bash
# Windows PowerShell
Copy-Item .env.example .env

# Linux / macOS
cp .env.example .env
```

### 5. Apply Database Migrations
```bash
python manage.py migrate
```

### 6. Create Default Admin Superuser
```bash
python manage.py create_default_admin
```
*(Default credentials set in `.env`: `admin` / `admin@kplonline.org` / `KPLAdmin@2026#Secure!`)*

---

## Running the Application

Start the development server:
```bash
python manage.py runserver
```

Visit the application in your browser:
- **Public Site**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Django Administration**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Running Tests
Run the automated test suite:
```bash
python manage.py test
```

Perform system diagnostic checks:
```bash
python manage.py check
```

---

## Deploy on Render

The repository includes a [Render Blueprint](https://render.com/docs/blueprint-spec) (`render.yaml`) that creates:

- a **free** Python web service running Gunicorn
- a **free** PostgreSQL database in Frankfurt
- a generated `SECRET_KEY`, with `DEBUG=False`

Static files are served by WhiteNoise. Local development still uses SQLite until `DATABASE_URL` or `DB_NAME` is set.

### 1. Push the project to Git

Render deploys from GitHub, GitLab, Bitbucket, or Cursor. Commit these files and push them: `render.yaml`, `build.sh`, `.python-version`, `requirements.txt`, and the Django project.

### 2. Create the Blueprint

1. In the [Render Dashboard](https://dashboard.render.com/), choose **New** → **Blueprint**.
2. Connect the repository and select it.
3. When prompted, set `DEFAULT_ADMIN_PASSWORD` to a strong password. Render stores it as an environment variable and does not read it from git.
4. Apply the Blueprint.

The first build installs dependencies, runs `collectstatic`, applies migrations, and creates the admin user if that password is set. The site is then available at `https://kpl-website.onrender.com` (Render may append a suffix if that name is taken).

Open `/admin/` and sign in with username `admin` and the password you set.

### 3. Custom domain

In the Render service settings, add the domain, then set:

- `ALLOWED_HOSTS` to that hostname (comma-separated if you have more than one)
- `CSRF_TRUSTED_ORIGINS` to `https://your-domain.example`

The `onrender.com` hostname is added automatically.

### Uploaded files

Membership documents, event images, and profile photos are stored in `media/` and served by the app. On the free web service that directory is wiped on every restart or redeploy. To keep uploads, change `plan` in `render.yaml` from `free` to a paid plan such as `0.5c-512mb` and uncomment the `disk` block. Persistent disks are not available on the free plan.

### Free-tier limits

The free web service sleeps after a period of inactivity, so the first visit can take a minute. Confirm Render's current free database limits in the dashboard before relying on it for live membership data. To change region, edit `render.yaml` before the first Blueprint apply. Region cannot be changed afterward.
