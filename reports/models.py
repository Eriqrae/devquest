from django.db import models

from users.abstracts import UniversalIdModel, TimeStampedModel
from classroom.settings import AUTH_USER_MODEL


class Report(UniversalIdModel, TimeStampedModel):
    student = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.TextField()
    problems = models.TextField(blank=True, null=True)
    solutions = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)

    class Meta:
        ordering = [
            "-created_at",
        ]

    def __str__(self) -> str:
        return self.student.first_name
