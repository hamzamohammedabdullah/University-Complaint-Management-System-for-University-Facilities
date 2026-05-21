from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for the custom User model.

    Extends Django's built-in UserAdmin to show the extra fields defined
    on the project's User model (role, student_id, department, phone).
    """
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Additional info", {"fields": ("role", "student_id", "department", "phone")} ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {"fields": ("role", "student_id", "department", "phone")} ),
    )

    list_display = ("username", "email", "get_full_name", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email", "student_id")
