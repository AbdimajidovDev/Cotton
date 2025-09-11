from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("full_name", "username", "phone_number", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("full_name", "phone_number", "image", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "full_name", "phone_number", "role", "password1", "password2", "is_staff",
                       "is_superuser"),
        }),
    )

    search_fields = ("username", "full_name", "phone_number")
    ordering = ("-id",)
