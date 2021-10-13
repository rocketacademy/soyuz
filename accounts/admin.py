from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Account
from .forms import UserCreationForm, UserChangeForm


class AccountAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'github_username', 'hubspot_id',
                    'is_staff',  'is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password')}),
        ('Personal info', {
         'fields': ('github_username', 'hubspot_id')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'is_staff',
         'is_superuser', 'password1', 'password2')}),
        ('Personal info', {
         'fields': ('github_username', 'hubspot_id')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('email', 'github_username', 'hubspot_id')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Account, AccountAdmin)
