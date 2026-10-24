# Organisational Risk Tracking and Reporting System

A beginner-friendly Django application for a college Security Risk Management project.

## Features
- Login-protected dashboard and risk register
- Automatic risk score = likelihood × impact
- Risk levels: Low (1–5), Medium (6–11), High (12–19), Critical (20–25)
- Add, view, edit and delete risk records
- Search and filter by category, status and level
- Dashboard KPIs and Chart.js charts
- CSV export
- Fictional sample-data command

## Run locally (Windows)
1. Install Python 3 and Git.
2. Open this folder in VS Code.
3. In the terminal run:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py load_sample_data
   python manage.py runserver
   ```
4. Open http://127.0.0.1:8000/ and sign in using the superuser account.

If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`.

## Demo flow
1. Sign in.
2. Open Risk Register.
3. Add a risk with likelihood 4 and impact 5.
4. Save and confirm score 20 / Critical.
5. Return to dashboard and confirm the KPI/chart values change.
6. Edit a risk's likelihood or status and observe the changes.

## Important limitations
- This is a local classroom prototype, not a production-ready risk platform.
- All logged-in users can currently manage risk records; role-based viewer permissions are not implemented yet.
- For production, set a private secret key in environment variables, set DEBUG=False, configure ALLOWED_HOSTS, use HTTPS, review permissions, and use a persistent production database.
- Chart.js and Bootstrap are loaded from CDNs, so the first page load needs an internet connection.
- The sample risks are fictional.
