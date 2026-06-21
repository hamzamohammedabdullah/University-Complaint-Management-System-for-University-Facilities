from django import forms
from .models import Complaint

class SubmitComplaintForm(forms.ModelForm):
    class Meta:
        model  = Complaint
        # priority is now auto-classified; remove it from the public form
        fields = ['category', 'building', 'location', 'description']
        widgets = {
            'category':    forms.Select(attrs={'class': 'form-select'}),
            # priority widget removed
            'building':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Engineering Block A'}),
            'location':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Room 204, Lab 3, Male Washroom'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe the issue in detail...'}),
        }

class UpdateStatusForm(forms.Form):
    STATUS_CHOICES = [
        ('Under Review', 'Under Review'),
        ('Assigned',     'Assigned'),
        ('In Progress',  'In Progress'),
        ('Resolved',     'Resolved'),
        ('Closed',       'Closed'),
        ('Escalated',    'Escalated'),
    ]
    status           = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    notes            = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Internal notes (optional)'}))
    resolution_notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe what was done to resolve the issue...'}))

class AssignComplaintForm(forms.Form):
    staff_id = forms.IntegerField(widget=forms.Select(attrs={'class': 'form-select'}))
    notes    = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))

    def __init__(self, staff_qs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['staff_id'].widget.choices = [('', '— Select staff member —')] + [(s.id, f"{s.get_full_name()} ({s.department})") for s in staff_qs]
