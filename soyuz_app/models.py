from django.db import models

# Create your models here.


class Course (models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Batch(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course_id = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)


class Section (models.Model):
    name = models.TextField()
    batch_id = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User (models.Model):
    github_username = models.CharField(max_length=200)
    batch_id = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)
    section_id = models.ForeignKey(
        Section, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Workflow_types (models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course_id = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)


class Workflows (models.Model):
    workFlow_type_id = models.CharField(max_length=200)
    completed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
