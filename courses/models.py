from django.db import models
from users.abstracts import UniversalIdModel, TimeStampedModel
from cloudinary.models import CloudinaryField
from django.urls import reverse

from classroom.settings import AUTH_USER_MODEL


class Resources(UniversalIdModel):
    name = models.CharField(max_length=255)
    link_one = models.URLField(max_length=1000, blank=True, null=True)
    link_two = models.URLField(max_length=1000, blank=True, null=True)
    link_three = models.URLField(max_length=1000, blank=True, null=True)
    course_notes = CloudinaryField("resources", blank=True, null=True)
    created_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resources"
    )

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("resources-detail", args=[str(self.id)])


class Lesson(UniversalIdModel):
    topic = models.CharField(max_length=255)
    objectives = models.TextField()
    resources = models.ManyToManyField(Resources, related_name="links", blank=True)
    created_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lessons"
    )

    def __str__(self) -> str:
        return self.topic

    def get_absolute_url(self):
        return reverse("lesson-detail", args=[str(self.id)])


class Unit(UniversalIdModel, TimeStampedModel):
    name = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)
    lessons = models.ManyToManyField(Lesson, related_name="topics", blank=True)
    created_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="units"
    )

    class Meta:
        ordering = [
            "-created_at",
        ]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("unit-detail", args=[str(self.id)])
