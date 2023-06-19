from django.db import models
from cloudinary.models import CloudinaryField

from classroom.settings import AUTH_USER_MODEL
from users.abstracts import UniversalIdModel, TimeStampedModel


class Task(UniversalIdModel, TimeStampedModel):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    document = CloudinaryField("task", blank=True, null=True)
    task_link = models.URLField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("submitted", "Submitted"),
            ("approved", "Approved"),
            ("disapproved", "Disapproved"),
        ],
        default="pending",
    )

    def is_submitted_by(self, student):
        return TaskSubmission.objects.filter(task=self, student=student).exists()

    def __str__(self) -> str:
        return self.title


class TaskSubmission(UniversalIdModel, TimeStampedModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = CloudinaryField("submission", blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    # add a field to state challenges faced

    class Meta:
        unique_together = ["task", "student"]

    def __str__(self) -> str:
        return self.task.title
