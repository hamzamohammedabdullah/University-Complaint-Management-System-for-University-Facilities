from django.db import models
from django.conf import settings
from django.utils import timezone

class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('Electrical',         'Electrical'),
        ('Plumbing',           'Plumbing'),
        ('ICT Infrastructure', 'ICT Infrastructure'),
        ('General Maintenance','General Maintenance'),
        ('Sanitation',         'Sanitation'),
        ('Security',           'Security'),
        ('Other',              'Other'),
    ]
    PRIORITY_CHOICES = [
        ('Low',    'Low'),
        ('Medium', 'Medium'),
        ('High',   'High'),
        ('Urgent', 'Urgent'),
    ]
    STATUS_CHOICES = [
        ('Submitted',    'Submitted'),
        ('Under Review', 'Under Review'),
        ('Assigned',     'Assigned'),
        ('In Progress',  'In Progress'),
        ('Resolved',     'Resolved'),
        ('Closed',       'Closed'),
        ('Escalated',    'Escalated'),
    ]

    complaint_id     = models.CharField(max_length=30, unique=True, editable=False)
    submitter        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    category         = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    priority         = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    location         = models.CharField(max_length=200)
    building         = models.CharField(max_length=100, blank=True)
    description      = models.TextField()
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Submitted')
    assigned_to      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints')
    assigned_dept    = models.CharField(max_length=50, blank=True)
    resolution_notes = models.TextField(blank=True)
    resolved_at      = models.DateTimeField(null=True, blank=True)
    is_escalated     = models.BooleanField(default=False)
    escalation_note  = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.complaint_id} — {self.category} ({self.status})"

    def save(self, *args, **kwargs):
        if not self.complaint_id:
            count = Complaint.objects.count() + 1
            year  = timezone.now().year
            self.complaint_id = f"CMS-{count:04d}-{year}"
        super().save(*args, **kwargs)

    @property
    def status_badge(self):
        mapping = {
            'Submitted':    'primary',
            'Under Review': 'warning',
            'Assigned':     'info',
            'In Progress':  'warning',
            'Resolved':     'success',
            'Closed':       'secondary',
            'Escalated':    'danger',
        }
        return mapping.get(self.status, 'secondary')

    @property
    def priority_badge(self):
        return {'Low':'success','Medium':'primary','High':'warning','Urgent':'danger'}.get(self.priority,'secondary')


class ComplaintMedia(models.Model):
    complaint     = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='media_files')
    file          = models.FileField(upload_to='uploads/%Y/%m/')
    original_name = models.CharField(max_length=255)
    uploaded_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name

    @property
    def is_image(self):
        return self.original_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))


class AuditLog(models.Model):
    complaint       = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='audit_logs')
    actor           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    actor_name      = models.CharField(max_length=100)
    action          = models.CharField(max_length=200)
    previous_status = models.CharField(max_length=20, blank=True)
    new_status      = models.CharField(max_length=20, blank=True)
    notes           = models.TextField(blank=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.complaint.complaint_id} — {self.action}"


class Notification(models.Model):
    TYPE_CHOICES = [
        ('status_update', 'Status Update'),
        ('assignment',    'Assignment'),
        ('resolution',    'Resolution'),
        ('escalation',    'Escalation'),
        ('general',       'General'),
    ]
    recipient    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    complaint    = models.ForeignKey(Complaint, on_delete=models.CASCADE, null=True, blank=True)
    title        = models.CharField(max_length=200)
    message      = models.TextField()
    notif_type   = models.CharField(max_length=20, choices=TYPE_CHOICES, default='general')
    is_read      = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"To {self.recipient.username}: {self.title}"
