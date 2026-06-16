from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Complaint, ComplaintMedia, AuditLog, Notification


def export_complaints_as_csv(modeladmin, request, queryset):
    """Admin action to export selected complaints as a CSV file."""
    fieldnames = [
        'complaint_id', 'student_username', 'student_email', 'category', 'priority',
        'location', 'building', 'status', 'assigned_to', 'assigned_dept',
        'is_escalated', 'created_at', 'resolved_at', 'resolution_notes', 'media_count', 'audit_count'
    ]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=complaints_export.csv'

    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()

    for c in queryset.select_related('student', 'assigned_to').prefetch_related('media_files', 'audit_logs'):
        writer.writerow({
            'complaint_id': c.complaint_id,
            'student_username': getattr(c.student, 'username', ''),
            'student_email': getattr(c.student, 'email', ''),
            'category': c.category,
            'priority': c.priority,
            'location': c.location,
            'building': c.building,
            'status': c.status,
            'assigned_to': getattr(c.assigned_to, 'username', '') if c.assigned_to else '',
            'assigned_dept': c.assigned_dept,
            'is_escalated': c.is_escalated,
            'created_at': c.created_at.isoformat() if c.created_at else '',
            'resolved_at': c.resolved_at.isoformat() if c.resolved_at else '',
            'resolution_notes': c.resolution_notes,
            'media_count': c.media_files.count(),
            'audit_count': c.audit_logs.count(),
        })

    return response


export_complaints_as_csv.short_description = 'Export selected complaints to CSV'


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('complaint_id', 'category', 'priority', 'status', 'student', 'assigned_to', 'created_at')
    list_filter = ('category', 'priority', 'status', 'is_escalated')
    search_fields = ('complaint_id', 'student__username', 'location', 'description')
    actions = [export_complaints_as_csv]
