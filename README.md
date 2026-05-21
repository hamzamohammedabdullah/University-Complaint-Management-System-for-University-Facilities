# UniCMS — Web-Based Complaint Management System for University Facilities
### Django + SQLite + Bootstrap 5 | Group 8 — BSc Computer Science

---

##  Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Backend    | Python + Django 4.2     |
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

### Step 1 — Install Django

Open a terminal inside the `unicms-django` folder and run:

```bash
pip install -r requirements.txt
```

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

Open your browser at **http://127.0.0.1:8000** 🎉

---

##  User Roles & How to Create Them

| Role      | How to create                               | What they can do                              |
|-----------|---------------------------------------------|-----------------------------------------------|
| `student` | Self-register at `/accounts/register/`      | Submit, track and view own complaints         |
| `staff`   | Admin creates via Manage Users page         | View assigned complaints, update status       |
| `admin`   | Via `createsuperuser` command               | Full access — assign, analytics, manage users |

To create staff accounts:
1. Log in as admin
2. Go to **Manage Users → Add User**
3. Set role to "Facilities Staff" and pick a department

---

##  URL Reference

| URL                        | Page                    | Access       |
|----------------------------|-------------------------|--------------|
| `/`                        | Redirect to dashboard   | Private      |
| `/accounts/login/`         | Login page              | Public       |
| `/accounts/register/`      | Student registration    | Public       |
| `/accounts/logout/`        | Sign out                | Private      |
| `/accounts/profile/`       | My profile              | Private      |
| `/accounts/users/`         | Manage users            | Admin only   |
| `/accounts/users/create/`  | Create staff/admin      | Admin only   |
| `/dashboard/`              | Dashboard               | Private      |
| `/complaints/`             | List all complaints     | Private      |
| `/complaints/new/`         | Submit a complaint      | Student only |
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
- Role-based access control (student / staff / admin)
- Password hashing via Django's PBKDF2 algorithm
- File upload type and size validation
- Login required on all private pages

---

## Future Enhancements (Chapter 5)

- [ ] Mobile-responsive improvements
- [ ] AI complaint auto-classification (NLP)
- [ ] REST API with Django REST Framework
- [ ] Switch to PostgreSQL for production deployment

---

##  Group 8 — BSc Computer Science | 2025
