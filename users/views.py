from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


from users.forms import TeacherCreationForm, StudentCreationForm, SupervisorCreationForm
from users.models import Teacher, Student

from classroom.settings import AUTH_USER_MODEL


@login_required
def dashboard(request):
    return render(request, "users/dashboard.html")


class SignUpView(TemplateView):
    template_name = "registration/signup.html"


class TeacherSignUpView(SuccessMessageMixin, CreateView):
    model = AUTH_USER_MODEL
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


class StudentSignUpView(SuccessMessageMixin, CreateView):
    model = AUTH_USER_MODEL
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


class SupervisorSignUpView(SuccessMessageMixin, CreateView):
    model = AUTH_USER_MODEL
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
