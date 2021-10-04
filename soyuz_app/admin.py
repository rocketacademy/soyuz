from django.contrib import admin

# Register your models here.
from .models import Batch, Section, User


class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch_id', 'created_at', 'updated_at')


class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_id', 'start_date',
                    'created_at', 'updated_at')


class UserAdmin(admin.ModelAdmin):
    list_display = ('github_username', 'batch_id',
                    'section_id', 'created_at', 'updated_at')


# Register your models here.
admin.site.register(Batch, BatchAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(User, UserAdmin)
