from django.contrib import admin

from app.users.models import User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('login', 'full_name', 'role', 'phone_number')
    list_display = ('login', 'full_name', 'role', 'phone_number')
