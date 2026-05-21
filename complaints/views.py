from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from django.db.utils import OperationalError
from accounts.models import User
from .models import Complaint, ComplaintMedia, AuditLog, Notification
from .forms import SubmitComplaintForm, UpdateStatusForm, AssignComplaintForm

def add_notification(recipient, complaint, title, message, notif_type='general'):
    # Save in-app notification
    Notification.objects.create(recipient=recipient, complaint=complaint,
        title=title, message=message, notif_type=notif_type)

    # Try delivering via email and SMS if contact details are available
    try:
        from .notifications import send_email_notification, send_sms_notification
        email_sent = send_email_notification(getattr(recipient, 'email', None), title, message)
        sms_sent = send_sms_notification(getattr(recipient, 'phone', None), f"{title}: {message}")
    except Exception:
        # Do not let delivery failures break the request flow
        email_sent = sms_sent = False

def add_audit(complaint, actor, action, prev_status='', new_status='', notes=''):
    AuditLog.objects.create(complaint=complaint, actor=actor,
        actor_name=actor.get_full_name() or actor.username,
        action=action, previous_status=prev_status, new_status=new_status, notes=notes)

@login_required
def dashboard(request):
    user = request.user
    try:
        # main dashboard logic that may hit DB tables
        pass
    except OperationalError:
        # friendly fallback when DB tables (migrations) are missing
        messages.error(request, 'The database is not ready yet - some tables are missing. Please run migrations (python manage.py migrate).')
        # Render dashboard with empty data to avoid a 500 crash
        return render(request, 'complaints/dashboard.html', {
            'complaints': [], 'stats': {}, 'unread_count': 0
        })
    if user.is_student:
        complaints = Complaint.objects.filter(student=user)[:5]
        stats = {
            'total':    Complaint.objects.filter(student=user).count(),
            'open':     Complaint.objects.filter(student=user).exclude(status__in=['Resolved','Closed']).count(),
            'resolved': Complaint.objects.filter(student=user, status='Resolved').count(),
        }
    elif user.is_staff_member:
        complaints = Complaint.objects.filter(assigned_to=user)[:5]
        stats = {
            'assigned':    Complaint.objects.filter(assigned_to=user).count(),
            'in_progress': Complaint.objects.filter(assigned_to=user, status='In Progress').count(),
            'resolved':    Complaint.objects.filter(assigned_to=user, status='Resolved').count(),
        }
    else:
        complaints = Complaint.objects.all()[:5]
        stats = {
            'total':       Complaint.objects.count(),
            'submitted':   Complaint.objects.filter(status='Submitted').count(),
            'in_progress': Complaint.objects.filter(status='In Progress').count(),
            'resolved':    Complaint.objects.filter(status='Resolved').count(),
            'escalated':   Complaint.objects.filter(is_escalated=True).count(),
        }
    unread_count = Notification.objects.filter(recipient=user, is_read=False).count()
    return render(request, 'complaints/dashboard.html',
        {'complaints': complaints, 'stats': stats, 'unread_count': unread_count})

@login_required
def complaints_list(request):
    user = request.user
    qs = Complaint.objects.all()
    if user.is_student:      qs = qs.filter(student=user)
    elif user.is_staff_member: qs = qs.filter(assigned_to=user)
    status_filter   = request.GET.get('status', '')
    category_filter = request.GET.get('category', '')
    search          = request.GET.get('search', '')
    if status_filter:   qs = qs.filter(status=status_filter)
    if category_filter: qs = qs.filter(category=category_filter)
    if search:
        qs = qs.filter(Q(complaint_id__icontains=search)|Q(location__icontains=search)|Q(description__icontains=search))
    return render(request, 'complaints/list.html', {
        'complaints': qs, 'status_filter': status_filter,
        'category_filter': category_filter, 'search': search,
        'statuses':   [c[0] for c in Complaint.STATUS_CHOICES],
        'categories': [c[0] for c in Complaint.CATEGORY_CHOICES],
        'unread_count': Notification.objects.filter(recipient=user, is_read=False).count(),
    })

@login_required
def submit_complaint(request):
    if not request.user.is_student:
        messages.error(request, 'Only students can submit complaints.')
        return redirect('dashboard')
    form = SubmitComplaintForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        complaint = form.save(commit=False)
        complaint.student = request.user
        complaint.save()
        for f in request.FILES.getlist('media'):
            ComplaintMedia.objects.create(complaint=complaint, file=f, original_name=f.name)
        add_audit(complaint, request.user, 'Complaint submitted', new_status='Submitted')
        messages.success(request, f'Complaint {complaint.complaint_id} submitted successfully!')
        return redirect('complaint_detail', pk=complaint.pk)
    return render(request, 'complaints/submit.html', {
        'form': form,
        'unread_count': Notification.objects.filter(recipient=request.user, is_read=False).count(),
    })

@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    user      = request.user
    if user.is_student and complaint.student != user:
        messages.error(request, 'You are not authorised to view this complaint.')
        return redirect('complaints_list')
    staff_qs    = User.objects.filter(role='staff', is_active=True)
    status_form = UpdateStatusForm()

    if request.method == 'POST' and (user.is_staff_member or user.is_admin):
        action = request.POST.get('action')
        if action == 'update_status':
            status_form = UpdateStatusForm(request.POST)
            if status_form.is_valid():
                prev = complaint.status
                new  = status_form.cleaned_data['status']
                complaint.status = new
                if status_form.cleaned_data.get('resolution_notes'):
                    complaint.resolution_notes = status_form.cleaned_data['resolution_notes']
                if new == 'Resolved':
                    complaint.resolved_at = timezone.now()
                complaint.save()
                add_audit(complaint, user, f'Status updated to {new}', prev, new, status_form.cleaned_data.get('notes',''))
                add_notification(complaint.student, complaint, f'Complaint {complaint.complaint_id} Updated',
                    f'Your complaint status changed from "{prev}" to "{new}".', 'status_update')
                messages.success(request, f'Status updated to {new}.')
                return redirect('complaint_detail', pk=pk)
        elif action == 'assign' and user.is_admin:
            staff_id = request.POST.get('staff_id')
            notes    = request.POST.get('notes', '')
            if staff_id:
                staff = get_object_or_404(User, id=staff_id, role='staff')
                prev  = complaint.status
                complaint.assigned_to = staff
                complaint.assigned_dept = staff.department
                complaint.status = 'Assigned'
                complaint.save()
                add_audit(complaint, user, f'Assigned to {staff.get_full_name()}', prev, 'Assigned', notes)
                add_notification(complaint.student, complaint, 'Complaint Assigned',
                    f'Your complaint {complaint.complaint_id} has been assigned to {staff.department}.', 'assignment')
                add_notification(staff, complaint, 'New Complaint Assigned',
                    f'Complaint {complaint.complaint_id} ({complaint.category}) assigned to you.', 'assignment')
                messages.success(request, f'Assigned to {staff.get_full_name()}.')
                return redirect('complaint_detail', pk=pk)
            else:
                messages.error(request, 'Please select a staff member.')
        elif action == 'escalate':
            note = request.POST.get('escalation_note', '')
            complaint.is_escalated = True
            complaint.escalation_note = note
            complaint.status = 'Escalated'
            complaint.save()
            add_audit(complaint, user, 'Complaint escalated', notes=note)
            messages.warning(request, 'Complaint has been escalated.')
            return redirect('complaint_detail', pk=pk)

    details_list = [
        ('Category',      complaint.category),
        ('Location',      complaint.location),
        ('Building',      complaint.building or '—'),
        ('Submitted By',  complaint.student.get_full_name()),
        ('Student ID',    complaint.student.student_id or '—'),
        ('Date Submitted',complaint.created_at.strftime('%d %b %Y, %H:%M')),
        ('Assigned To',   complaint.assigned_to.get_full_name() if complaint.assigned_to else 'Unassigned'),
        ('Department',    complaint.assigned_dept or '—'),
    ]

    return render(request, 'complaints/detail.html', {
        'complaint':    complaint,
        'audit_logs':   complaint.audit_logs.all(),
        'media_files':  complaint.media_files.all(),
        'status_form':  status_form,
        'staff_list':   staff_qs,
        'details_list': details_list,
        'unread_count': Notification.objects.filter(recipient=user, is_read=False).count(),
    })

@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    by_status   = list(Complaint.objects.values('status').annotate(count=Count('id')))
    by_category = list(Complaint.objects.values('category').annotate(count=Count('id')).order_by('-count'))
    stats = {
        'total':       Complaint.objects.count(),
        'submitted':   Complaint.objects.filter(status='Submitted').count(),
        'in_progress': Complaint.objects.filter(status='In Progress').count(),
        'resolved':    Complaint.objects.filter(status='Resolved').count(),
        'closed':      Complaint.objects.filter(status='Closed').count(),
        'escalated':   Complaint.objects.filter(is_escalated=True).count(),
    }
    return render(request, 'complaints/admin_dashboard.html', {
        'stats': stats, 'by_status': by_status, 'by_category': by_category,
        'unread_count': Notification.objects.filter(recipient=request.user, is_read=False).count(),
    })

@login_required
def notifications_view(request):
    notifs = Notification.objects.filter(recipient=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'mark_all':
            notifs.update(is_read=True)
            messages.success(request, 'All notifications marked as read.')
        elif action == 'mark_one':
            nid = request.POST.get('notif_id')
            Notification.objects.filter(id=nid, recipient=request.user).update(is_read=True)
        return redirect('notifications')
    return render(request, 'complaints/notifications.html', {
        'notifications': notifs,
        'unread_count':  notifs.filter(is_read=False).count(),
    })
