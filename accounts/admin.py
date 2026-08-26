from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_approved", "is_staff")
    list_filter = ("role", "is_approved")
    fieldsets = UserAdmin.fieldsets + (
        ("Rol y aprobación", {"fields": ("role", "is_approved", "approved_by")}),
    )


admin.site.register(User, CustomUserAdmin)