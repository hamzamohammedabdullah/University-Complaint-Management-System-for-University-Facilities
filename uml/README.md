# UML diagrams for UniCMS project

This folder contains PlantUML (.puml) files that document the main data models, system components, and key flows of the UniCMS Django project. They are intended to be used in a thesis or documentation.

Files:

- `accounts_class.puml` — Class diagram for the `accounts.User` model and relationships.
- `complaints_class.puml` — Class diagram for complaints-related models: `Complaint`, `ComplaintMedia`, `AuditLog`, `Notification`.
- `system_components.puml` — Component diagram showing the Django project, apps, database and external services (SMTP, Twilio).
- `seq_login.puml` — Sequence diagram for the login flow.
- `seq_register.puml` — Sequence diagram for user registration.
- `seq_submit_complaint.puml` — Sequence diagram for complaint submission (with media uploads).
- `seq_notification.puml` — Sequence diagram for notification creation and delivery (email/SMS fallback).

Rendering

Option 1: Use the PlantUML jar (recommended for offline rendering)

1. Install Graphviz (for PNG/SVG output of some diagrams). Ensure `dot` is in your PATH.
2. Download PlantUML: https://plantuml.com/download
3. Render a diagram:

```powershell
java -jar plantuml.jar accounts_class.puml
```

Option 2: Use an online PlantUML renderer or VS Code PlantUML extension.

Notes for thesis

- The class diagrams list the main fields and key helper methods. For full field types and behavior, refer to the source files in `accounts/models.py` and `complaints/models.py`.
- The sequence diagrams show the happy-path flows. If you need more detail (e.g., form validation branches, error handling, or database transaction boundaries), tell me which flow to expand.

If you'd like, I can also generate PNG/SVG files here and add them to the repo, or produce higher-resolution diagrams with expanded labels suitable for print.
