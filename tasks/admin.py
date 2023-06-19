from django.contrib import admin

from tasks.models import Task, TaskSubmission

admin.site.register(Task)
admin.site.register(TaskSubmission)