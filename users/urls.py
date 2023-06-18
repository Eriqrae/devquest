from django.urls import path

from users.views import (
    TeacherSignUpView,
    dashboard,
    SignUpView,
    StudentSignUpView,
    SupervisorSignUpView,
    UserDetailView,
    UserListView,
    TeacherDetailView,
    TeacherDeleteView,
    TeacherUpdateView,
    StudentDeleteView,
    StudentDetailView,
    StudentUpdateView,
)

app_name = "users"

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signup/teacher/", TeacherSignUpView.as_view(), name="teacher-signup"),
    path("signup/student/", StudentSignUpView.as_view(), name="student-signup"),
    path(
        "signup/supervisor/", SupervisorSignUpView.as_view(), name="supervisor-signup"
    ),
    path("users/", UserListView.as_view(), name="users"),
    path("user/<str:pk>/detail/", UserDetailView.as_view(), name="user-detail"),
    path(
        "profile/<str:pk>/student/", StudentDetailView.as_view(), name="student-profile"
    ),
    path(
        "update/<str:pk>/student/", StudentUpdateView.as_view(), name="student-update"
    ),
    path(
        "delete/<str:pk>/student/", StudentDeleteView.as_view(), name="student-delete"
    ),
    path(
        "teacher/<str:pk>/profile/", TeacherDetailView.as_view(), name="teacher-profile"
    ),
    path(
        "teacher/<str:pk>/update/", TeacherUpdateView.as_view(), name="teacher-update"
    ),
    path(
        "teacher/<str:pk>/delete/", TeacherDeleteView.as_view(), name="teacher-delete"
    ),
]
