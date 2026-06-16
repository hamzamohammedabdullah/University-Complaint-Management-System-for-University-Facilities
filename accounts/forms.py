from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class FacilityUserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name  = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email      = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'you@university.edu.gh'}))
    facility_id = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'e.g. UG0574822'}))
    phone      = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': '+233 XX XXX XXXX'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'facility_id', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email      = self.cleaned_data['email']
        user.facility_id = self.cleaned_data.get('facility_id', '')
        user.phone      = self.cleaned_data.get('phone', '')
        # new default role for self-registering users is 'facility' (facility users)
        user.role       = 'facility'
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))

class CreateStaffForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name  = forms.CharField(max_length=50, required=True)
    email      = forms.EmailField(required=True)
    role       = forms.ChoiceField(choices=[('staff', 'Facilities Staff'), ('admin', 'Administrator')])
    department = forms.ChoiceField(choices=[('', '— Select —')] + User.DEPARTMENT_CHOICES, required=False)

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'username', 'email', 'role', 'department', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role       = self.cleaned_data['role']
        user.department = self.cleaned_data.get('department', '')
        if commit:
            user.save()
        return user
