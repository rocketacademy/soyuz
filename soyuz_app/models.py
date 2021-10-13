from django.db import models
from django.conf import settings
from django.db.models.deletion import PROTECT

# Create your models here.


class Course (models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# class User (models.Model):
#     github_username = models.CharField(max_length=200)
#     email = models.EmailField(max_length=200)
#     hubspot_id = models.TextField(max_length=300, null=True)


class Batch(models.Model):
    number = models.IntegerField()
    start_date = models.DateField()
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)


class Section (models.Model):
    number = models.IntegerField()
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True)
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE)


class Workflow_type (models.Model):
    name = models.CharField(max_length=200)
    course_id = models.ManyToManyField(Course)


class Workflows (models.Model):
    workFlow_type_id = models.ForeignKey(Workflow_type, on_delete=PROTECT)
    completed = models.BooleanField(default=False)
