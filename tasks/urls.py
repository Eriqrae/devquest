from django.urls import path
from tasks.views import (
    TaskCreateView,
    TaskDetailView,
    TaskSubmissionCreateView,
    TaskSubmissionApproveView,
    TaskSubmissionListView,
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
        "activity/tasks/submissions/<str:pk>/approve/",
        TaskSubmissionApproveView.as_view(),
        name="task-submission-approve",
    ),
    path(
        "activity/tasks/submissions/<str:pk>/disapprove/",
        TaskSubmissionApproveView.as_view(),
        name="task-submission-disapprove",
    ),
]
