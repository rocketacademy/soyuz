from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db.models.deletion import PROTECT
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError("Userz must have an email address")
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    hubspot_id = models.CharField(max_length=200, null=True, blank=True)
    github_username = models.CharField(max_length=200, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)


class Course(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Batch(models.Model):
    number = models.IntegerField()
    start_date = models.DateField()
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

    def add_student_to_section(self, user):

        max_students = settings.MAX_STUDENTS_SECTION

        section = self.section_set.order_by("id").last()
        if section is not None and section.users.count() < max_students:
            # section that still has space left
            section.users.add(user)

        # no sections yet or all sections full
        else:

            section_num = section.number + 1 if section is not None else 1
            section = Section.objects.create(number=section_num, batch_id=self)
            section.users.add(user)

        return section


class Section(models.Model):
    number = models.IntegerField()
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE)


class Workflow_type(models.Model):
    name = models.CharField(max_length=200)
    course_id = models.ManyToManyField(Course)


class Workflows(models.Model):
    workFlow_type_id = models.ForeignKey(Workflow_type, on_delete=PROTECT)
    completed = models.BooleanField(default=False)
