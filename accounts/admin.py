
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "display_name",
        "is_staff",
        "is_active",
    )

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {
            "fields": ("display_name",),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Information", {
            "fields": ("display_name",),
        }),
    )
