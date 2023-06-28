from django.shortcuts import render, redirect
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.timezone import now


from users.forms import TeacherCreationForm, StudentCreationForm, SupervisorCreationForm
from users.models import Teacher, Student
from tasks.models import Task
from courses.models import Unit
from reports.models import Report

User = get_user_model()


@login_required
def dashboard(request):
    units = Unit.objects.all()[0:3]
    tasks = Task.objects.all()[0:6]
    reports = Report.objects.filter(student=request.user)
    entries = Report.objects.all()
    return render(
        request,
        "users/dashboard.html",
        {
            "tasks": tasks,
            "now": now(),
            "units": units,
            "reports": reports,
            "entries": entries,
        },
    )


class UserListView(UserPassesTestMixin, ListView, LoginRequiredMixin):
    """admin sees all users"""

    model = User
    template_name = "users/users_list.html"

    def test_func(self):
        return self.request.user.is_staff


class UserDetailView(UserPassesTestMixin, DetailView):
    """details on specific users"""

    model = User
    template_name = "users/user_detail.html"

    def test_func(self):
        return self.request.user.is_staff


class SignUpView(TemplateView):
    template_name = "registration/signup.html"


class TeacherSignUpView(SuccessMessageMixin, CreateView):
    model = User
    form_class = TeacherCreationForm
    template_name = "registration/signup_form.html"
    success_message = "Account Created"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "teacher"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("users:dashboard")


class TeacherDetailView(LoginRequiredMixin, DetailView):
    """Teacher views their details"""

    model = Teacher
    fields = [
        "image",
        "phonenumber",
        "github",
        "qualifications",
        "about",
    ]
    template_name = "users/teacher_profile.html"


class TeacherUpdateView(
    SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView
):
    """Teacher updates profile"""

    model = Teacher
    fields = [
        "image",
        "phonenumber",
        "github",
        "qualifications",
        "about",
    ]
    template_name = "users/teacher_update.html"
    success_message = "Profile Updated Successfully"

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("users:teacher-profile", kwargs={"pk": self.object.pk})


class TeacherDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    """Teacher deletes their profile"""

    model = User
    template_name = "users/teacher_delete.html"
    success_url = reverse_lazy("login")

    def test_func(self):
        return self.request.user.is_teacher


class StudentSignUpView(SuccessMessageMixin, CreateView):
    model = User
    form_class = StudentCreationForm
    template_name = "registration/signup_form.html"
    success_message = "Account Created"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "student"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("users:dashboard")


class StudentDetailView(LoginRequiredMixin, DetailView):
    """View the details of the student"""

    model = Student
    fields = [
        "image",
        "phonenumber",
        "github",
        "about",
    ]
    template_name = "users/student_profile.html"


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    """student updates their profile"""

    model = Student
    fields = [
        "image",
        "phonenumber",
        "github",
        "about",
    ]
    template_name = "users/student_update.html"

    def test_func(self):
        return self.request.user.is_teacher

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("users:student-profile", kwargs={"pk": self.object.pk})


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    """student deletes their profile"""

    model = User
    template_name = "users/student_delete.html"
    success_url = reverse_lazy("login")


class SupervisorSignUpView(SuccessMessageMixin, CreateView):
    model = User
    form_class = SupervisorCreationForm
    template_name = "registration/signup_form.html"
    success_message = "Account Created"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "supervisor"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("users:dashboard")
