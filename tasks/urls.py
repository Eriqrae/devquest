from django.urls import path
from tasks.views import (
    TaskCreateView,
    TaskDetailView,
    TaskSubmissionDetailView,
    TaskSubmissionListView,
    TaskUpdateView,
    task_submission_create,
    task_list,
    mytasks,
)

app_name = "tasks"

urlpatterns = [
    path("tasks/", task_list, name="task-list"),
    path("mytasks/", mytasks, name="mytasks"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<str:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<str:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path(
        "tasks/submissions/list/",
        TaskSubmissionListView.as_view(),
        name="task-submission-list",
    ),
    path(
        "tasks/<str:task_id>/submit/",
        task_submission_create,
        name="task-submission-create",
    ),
    path(
        "tasks/<str:pk>/detail/",
        TaskSubmissionDetailView.as_view(),
        name="submission-detail",
    ),
]
