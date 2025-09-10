from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Admin'da ko‘rinadigan ustunlar
    list_display = ("full_name", "login", "phone_number", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")

    # Foydalanuvchi qo‘shishda va tahrirlaganda form maydonlari
    fieldsets = (
        (None, {"fields": ("login", "password")}),
        ("Personal info", {"fields": ("full_name", "phone_number", "image", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    # Yangi foydalanuvchi qo‘shishda ko‘rinadigan maydonlar
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("login", "full_name", "phone_number", "role", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )

    search_fields = ("login", "full_name", "phone_number")
    ordering = ("-id",)
