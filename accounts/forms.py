from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from .models import User


class FacilityUserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'you@university.edu.gh'}))
    facility_id = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g. UG0574822'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': '+233 XX XXX XXXX'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'facility_id', 'phone']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.facility_id = self.cleaned_data.get('facility_id', '')
        user.phone = self.cleaned_data.get('phone', '')
        user.role = 'facility'
        # set default password from settings or fallback
        default_pw = getattr(settings, 'DEFAULT_FACILITY_PASSWORD', 'ChangeMe123!')
        user.set_password(default_pw)
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))


class AltLoginForm(AuthenticationForm):
    """Alternative login form that includes a role dropdown.

    The role is not required to authenticate, but we enforce that the
    selected role matches the authenticated user's `role` property.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True, widget=forms.Select())

class CreateStaffForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[('facility', 'Facility User'), ('staff', 'Maintenance Staff'), ('admin', 'Administrator')])
    department = forms.ChoiceField(choices=[('', '— Select —')] + User.DEPARTMENT_CHOICES, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'role', 'department']

    def save(self, commit=True):
        user = super().save(commit=False)
        selected_role = self.cleaned_data.get('role')
        user.role = selected_role
        user.department = self.cleaned_data.get('department', '')
        # set default password depending on role
        default_staff_pw = getattr(settings, 'DEFAULT_STAFF_ADMIN_PASSWORD', 'AdminChangeMe123!')
        default_facility_pw = getattr(settings, 'DEFAULT_FACILITY_PASSWORD', 'ChangeMe123!')
        if selected_role == 'facility':
            user.set_password(default_facility_pw)
        else:
            user.set_password(default_staff_pw)
        if commit:
            user.save()
        return user
