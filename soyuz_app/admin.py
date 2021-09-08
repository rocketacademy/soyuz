from django.contrib import admin

# Register your models here.
from .models import Batch, Section

class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch', 'created_at', 'updated_at')

class BatchAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'created_at', 'updated_at')

# Register your models here.
admin.site.register(Batch, BatchAdmin)
admin.site.register(Section, SectionAdmin)
