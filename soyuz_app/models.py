from django.db import models

# Create your models here.
from django.db import models

class Section (models.Model):

    name = models.TextField()
    batch = models.ForeignKey("Batch", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Batch(models.Model):

    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
