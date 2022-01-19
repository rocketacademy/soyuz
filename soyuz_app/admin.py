from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from .models import Batch, Course, Section, User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "github_username",
                    "hubspot_id",
                    "slack_id",
                    "last_login",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )

    list_display = ("email", "hubspot_id", "github_username", "slack_id", "is_staff", "last_login")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


class SectionAdmin(admin.ModelAdmin):
    list_display = ("number", "batch")


class BatchAdmin(admin.ModelAdmin):
    list_display = ("number", "start_date", "course")


# class UserAdmin(admin.ModelAdmin):
#     list_display = ('github_username', 'hubspot_id')


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Course)
