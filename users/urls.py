from django.urls import path

from users.views import TeacherSignUpView, dashboard, SignUpView, StudentSignUpView, SupervisorSignUpView

app_name = "users"

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signup/teacher/", TeacherSignUpView.as_view(), name="teacher-signup"),
    path("signup/student/", StudentSignUpView.as_view(), name="student-signup"),
    path(
        "signup/supervisor/", SupervisorSignUpView.as_view(), name="supervisor-signup"
    ),
]
