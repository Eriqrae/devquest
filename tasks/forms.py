from django import forms
from .models import TaskSubmission, Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "deadline",
            "description",
            "document",
            "task_link",
        ]
        widgets = {"deadline": forms.DateInput(attrs={"type": "datetime-local"})}


class TaskSubmissionForm(forms.ModelForm):
    class Meta:
        model = TaskSubmission
        fields = [
            "links",
            "document",
            "answer",
        ]
