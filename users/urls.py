from django.urls import path

from users.views import TeacherSignUpView, dashboard, SignUpView

app_name = "users"

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signup/teacher/", TeacherSignUpView.as_view(), name="teacher-signup"),
]
