# UniCMS — Web-Based Complaint Management System for University Facilities
### Django + SQLite + Bootstrap 5 | Group 8 — BSc Computer Science

---

##  Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Backend    | Python + Django 6.0.3   |
| Database   | SQLite (built-in)       |
| Frontend   | HTML + Bootstrap 5      |
| Charts     | Chart.js (CDN)          |
| Icons      | Bootstrap Icons (CDN)   |

> **No MongoDB. No Node.js. No React.** Just Python + Django. One terminal.

---

##  Setup (3 steps only)

### What you need installed first:
- **Python 3.10+** → https://www.python.org/downloads/
- **VS Code** → https://code.visualstudio.com *(optional but recommended)*

---

### Step 1 — Install dependencies

Open a terminal inside the `unicms-django` folder and run:

```bash
pip install -r requirements.txt
```

Alternatively, for a one-click local setup on Windows, double-click `autorun.bat` in the project root. It will create a virtual environment, install the dependencies, run migrations, and start the application.

---

### Step 2 — Set up the database

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the `db.sqlite3` file automatically. No external database needed.

---

### Step 3 — Create your admin account

```bash
python manage.py createsuperuser
```

Enter a username, email, and password when prompted. This will be your admin login.

---

### Run the app

```bash
python manage.py runserver
```

Open your browser at **http://127.0.0.1:8000** 

### Quick launch with autorun

- Double-click `autorun.bat` from the project root on a Windows machine.
- The launcher will install dependencies, migrate the database, run checks, and open the app locally.
- You can also read the simple instructions in `README_AUTORUN.txt`.

---

##  User Roles & How to Create Them

| Role      | How to create                               | What they can do                              |
|-----------|---------------------------------------------|-----------------------------------------------|
| `facility` | Self-register at `/accounts/register/` or by a Maintenance Staff/Admin in Manage Users | Submit, track and view own complaints         |
| `staff`   | Admin or Maintenance Staff creates via Manage Users page | View assigned complaints, update status       |
| `admin`   | Via `createsuperuser` command               | Full access — assign, analytics, manage users |

To create staff accounts:
1. Log in as admin
2. Go to **Manage Users → Add User**
3. Set role to "Maintenance Staff" and pick a department

### Latest account-management updates
- The main login page at `/accounts/login/` now uses the alternate role-based login flow with a required role dropdown.
- Maintenance Staff and Administrators can create facility users directly from the Manage Users area.
- Facility and staff/admin accounts are assigned a default temporary password automatically during creation.
- Users receive an email with their temporary password, and first-time sign-ins trigger a reminder to update the password.
- Administrators can import multiple facility-user accounts from an Excel file using the batch upload feature.

---

##  URL Reference

| URL                        | Page                    | Access       |
|----------------------------|-------------------------|--------------|
| `/`                        | Redirect to dashboard   | Private      |
| `/accounts/login/`         | Main login page with role selection | Public       |
| `/accounts/alt-login/`     | Alias for the alternate login flow | Public       |
| `/accounts/register/`      | Facility user registration    | Public       |
| `/accounts/logout/`        | Sign out                | Private      |
| `/accounts/profile/`       | My profile              | Private      |
| `/accounts/users/`         | Manage users            | Admin only   |
| `/accounts/users/create/`  | Create staff/admin      | Admin only   |
| `/dashboard/`              | Dashboard               | Private      |
| `/complaints/`             | List all complaints     | Private      |
| `/complaints/new/`         | Submit a complaint      | Facility users only |
| `/complaints/<id>/`        | Complaint detail        | Private      |
| `/admin-panel/`            | Analytics dashboard     | Admin only   |
| `/notifications/`          | My notifications        | Private      |
| `/admin/`                  | Django admin panel      | Superuser    |

---

## Project Structure

```
unicms-django/
├── manage.py                  ← Run the app from here
├── requirements.txt           ← Python dependencies
├── db.sqlite3                 ← Auto-created database (after migrate)
├── media/uploads/             ← Uploaded complaint files
│
├── unicms/                    ← Project config
│   ├── settings.py
│   └── urls.py
│
├── accounts/                  ← User auth app
│   ├── models.py              ← Custom User model
│   ├── views.py               ← Register, login, user management
│   ├── forms.py
│   └── urls.py
│
├── complaints/                ← Main app
│   ├── models.py              ← Complaint, AuditLog, Notification
│   ├── views.py               ← All complaint logic
│   ├── forms.py
│   └── urls.py
│
└── templates/
    ├── layouts/base.html      ← Sidebar + navbar layout
    ├── accounts/              ← Login, register, users pages
    └── complaints/            ← Dashboard, list, detail, submit
```

---

## Complaint Lifecycle

```
Submitted → Under Review → Assigned → In Progress → Resolved → Closed
                                                  ↕
                                              Escalated
```

---

## Security Features

- Django's built-in CSRF protection on all forms
- Session-based authentication
- Role-based access control (facility / staff / admin)
- Password hashing via Django's PBKDF2 algorithm
- File upload type and size validation
- Login required on all private pages

---

## Recent system updates

- Role-based login is now the default sign-in experience.
- The system supports batch creation of facility-user accounts from Excel uploads.
- Temporary password assignment is automated for new accounts.
- Password update reminders are sent on first login.
- The project includes an autorun launcher for simple Windows startup.

## Future Enhancements (Chapter 5)

- [ ] Mobile-responsive improvements
- [ ] AI complaint auto-classification (NLP)
- [ ] REST API with Django REST Framework
- [ ] Switch to PostgreSQL for production deployment

---

##  Group 8 — BSc Computer Science | 2025

---

## Email (SMTP) setup

The app uses Django's email backend to send notification emails. You can configure SMTP in `unicms/settings.py` (recommended: use environment variables for secrets).

Example (Gmail / SMTP) — add to `settings.py` or load from env:

```python
import os

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')  # use app password
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'no-reply@example.com')
```

Development tip: to avoid sending real email during development, use the console backend:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Test sending an email from Django shell:

```bash
python manage.py shell
```
```python
from django.core.mail import send_mail
send_mail('Test email', 'This is a test', 'from@example.com', ['you@example.com'])
```

Security notes:
- Prefer environment variables or a secrets manager for credentials (do not commit passwords to VCS).
- For Gmail use an App Password (if using 2FA) rather than your main account password.
- Ensure your SMTP provider allows sending from the configured `DEFAULT_FROM_EMAIL`.

---

## Twilio (SMS) setup

Twilio is used for optional SMS notifications. Configure the credentials as environment variables and add them to `unicms/settings.py`:

```python
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_FROM_NUMBER = os.environ.get('TWILIO_FROM_NUMBER')  # E.164 format, e.g. +15551234567
```

Install the Twilio client (if not already installed):

```bash
pip install twilio
```

Test sending an SMS from Django shell:

```bash
python manage.py shell
```
```python
from twilio.rest import Client
import os
sid = os.environ.get('TWILIO_ACCOUNT_SID')
token = os.environ.get('TWILIO_AUTH_TOKEN')
from_num = os.environ.get('TWILIO_FROM_NUMBER')
client = Client(sid, token)
client.messages.create(body='Test message', from_=from_num, to='+19995551234')
```

Notes:
- The notification code falls back to logging SMS if Twilio is not configured; adding these env vars enables real delivery.
- Confirm your Twilio account has an active phone number and sufficient balance (if using paid numbers).
- Keep Twilio credentials secret — store them in environment variables or secrets management.

