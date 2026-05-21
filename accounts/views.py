from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StudentRegistrationForm, LoginForm, CreateStaffForm
from .models import User

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = StudentRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
        return redirect('dashboard')
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Welcome back, {user.first_name or user.username}!')
        return redirect(request.GET.get('next', 'dashboard'))
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been signed out.')
    return redirect('login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name  = request.POST.get('last_name', user.last_name)
        user.phone      = request.POST.get('phone', user.phone)
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'accounts/profile.html')

# Admin: list users
@login_required
def admin_users_view(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    role_filter = request.GET.get('role', '')
    users = User.objects.all().order_by('-date_joined')
    if role_filter:
        users = users.filter(role=role_filter)
    return render(request, 'accounts/admin_users.html', {'users': users, 'role_filter': role_filter})

# Admin: create staff/admin account
@login_required
def create_user_view(request):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    form = CreateStaffForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'User account created successfully.')
        return redirect('admin_users')
    return render(request, 'accounts/create_user.html', {'form': form})

# Admin: toggle active
@login_required
def toggle_user_view(request, user_id):
    if not request.user.is_admin:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    status = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'User {user.get_full_name()} has been {status}.')
    return redirect('admin_users')
