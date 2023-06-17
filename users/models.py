from django.db import models

from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField

from users.managers import CustomUserManager
from users.abstracts import UniversalIdModel, TimeStampedModel

from classroom.settings import AUTH_USER_MODEL


class CustomUser(AbstractUser, UniversalIdModel):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name


class Teacher(TimeStampedModel):
    """
    The instructor model
    """

    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="teacher",
    )
    image = CloudinaryField("teacher_image")
    phonenumber = models.BigIntegerField(default=0, blank=False)
    about = models.TextField(blank=True, null=True)
    qualifications = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return self.user.first_name


class Student(TimeStampedModel):
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="student",
    )
    image = CloudinaryField("student_image")
    phonenumber = models.BigIntegerField(default=0, blank=False)
    about = models.TextField(blank=True, null=True)


class Supervisor(TimeStampedModel):
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="supervisor",
    )
    phonenumber = models.BigIntegerField(default=0, blank=False)
