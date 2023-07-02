from django.db import models

from users.abstracts import UniversalIdModel, TimeStampedModel
from classroom.settings import AUTH_USER_MODEL


class Report(UniversalIdModel, TimeStampedModel):
    student = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.TextField(
        help_text="Provide a detailed description of the activities you have performed.",
    )
    problems = models.TextField(
        blank=True,
        null=True,
        help_text="Describe any challenges or difficulties you encountered during the activities.",
    )
    solutions = models.TextField(
        blank=True,
        null=True,
        help_text="If you were able to solve the problems, explain the solutions or approaches you used. If not, indicate the steps you took or any progress made towards finding a solution.",
    )
    response = models.TextField(
        blank=True,
        null=True,
        help_text="Add any response or feedback received related to the report, if applicable.",
    )

    class Meta:
        ordering = [
            "-created_at",
        ]

    def __str__(self) -> str:
        return self.student.first_name
