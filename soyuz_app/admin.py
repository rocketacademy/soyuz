from django.contrib import admin

# Register your models here.
from .models import Batch, Section, Course


class SectionAdmin(admin.ModelAdmin):
    list_display = ('number', 'batch_id')


class BatchAdmin(admin.ModelAdmin):
    list_display = ('number', 'start_date',
                    'course_id')


# class UserAdmin(admin.ModelAdmin):
#     list_display = ('github_username', 'hubspot_id')


# Register your models here.
admin.site.register(Batch, BatchAdmin)
admin.site.register(Section, SectionAdmin)
# admin.site.register(User, UserAdmin)
admin.site.register(Course)
