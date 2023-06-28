# from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)

from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from courses.models import Unit, Resources, Lesson
from courses.forms import ResourcesForm, LessonForm, UnitForm
from courses.decorators import teacher_required

"""
Resources section
used to build on lessons
creating
updating
listing
deleting
"""


@login_required
@teacher_required
def add_resource(request):
    if request.method == "POST":
        form = ResourcesForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.created_by = request.user
            resource.save()

            messages.success(request, "Resource added successfully")

            return redirect("courses:myresources")
    else:
        form = ResourcesForm()
    return render(request, "courses/resources_create.html", {"form": form})


class ResourcesListView(ListView):
    model = Resources
    fields = [
        "name",
        "link_one",
        "link_two",
        "link_three",
        "course_notes",
    ]
    template_name = "courses/resources_list.html"


def myresources(request):
    resources = Resources.objects.filter(created_by=request.user)
    return render(request, "courses/myresources.html", {"resources": resources})


class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = Resources
    fields = [
        "name",
        "link_one",
        "link_two",
        "link_three",
        "course_notes",
    ]
    template_name = "courses/resources_detail.html"


class ResourcesUpdateView(
    SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    model = Resources
    fields = [
        "name",
        "link_one",
        "link_two",
        "link_three",
        "course_notes",
    ]
    template_name = "courses/resources_update.html"
    success_message = "Resources Updated"
    success_url = reverse_lazy("courses:myresources")

    def test_func(self):
        return self.request.user.is_staff


class ResourcesDeleteView(
    SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    model = Resources
    template_name = "courses/resources_delete.html"
    success_message = "Resource Deleted"
    success_url = reverse_lazy("courses:myresources")

    def test_func(self):
        return self.request.user.is_staff


"""
lessons section
contain a combination of resources
creating
listing
updating
deletion
"""


@login_required
def mylessons(request):
    lessons = Lesson.objects.filter(created_by=request.user)
    return render(request, "courses/mylessons.html", {"lessons": lessons})


class LessonCreateView(
    SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView
):
    model = Lesson
    template_name = "courses/lesson_create.html"
    success_message = "Lesson Created"
    success_url = reverse_lazy("courses:mylessons")

    def test_func(self):
        return self.request.user.is_staff

    def get_form(self, form_class=LessonForm):
        form = super().get_form(form_class)
        form.fields["resources"].queryset = Resources.objects.filter(
            created_by=self.request.user
        )
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class LessonListView(ListView):
    model = Lesson
    fields = [
        "topic",
        "objectives",
        "resources",
    ]
    template_name = "courses/lesson_list.html"


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    fields = [
        "topic",
        "objectives",
        "resources",
    ]
    template_name = "courses/lesson_detail.html"


class LessonUpdateView(
    SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    model = Lesson
    template_name = "courses/lesson_update.html"
    success_message = "Lesson Updated"
    success_url = reverse_lazy("courses:mylessons")

    def test_func(self):
        return self.request.user.is_staff

    def get_form(self, form_class=LessonForm):
        form = super().get_form(form_class)
        form.fields["resources"].queryset = Resources.objects.filter(
            created_by=self.request.user
        )
        return form


class LessonDeleteView(
    SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    model = Lesson
    template_name = "courses/lesson_delete.html"
    success_message = "Lesson Deleted"
    success_url = reverse_lazy("courses:mylessons")

    def test_func(self):
        return self.request.user.is_staff


"""
Units/Courses section
creating units
listing units
updating units
deleting units
"""


@login_required
def unit_page(request):
    units = Unit.objects.filter(created_by=request.user)
    return render(request, "courses/my_units.html", {"units": units})


class UnitCreateView(
    SuccessMessageMixin, LoginRequiredMixin, CreateView, UserPassesTestMixin
):
    """
    creation of units
    only done by supervisors and teachers
    """

    model = Unit
    template_name = "courses/unit_create.html"
    success_message = "Unit Created"
    success_url = reverse_lazy("courses:my-units")

    def test_func(self):
        return self.request.user.is_staff

    def get_form(self, form_class=UnitForm):
        form = super().get_form(form_class)
        form.fields["lessons"].queryset = Lesson.objects.filter(
            created_by=self.request.user
        )
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class UnitListView(ListView):
    model = Unit
    fields = [
        "name",
        "duration",
        "lessons",
    ]
    template_name = "courses/units.html"


class UnitDetailView(DetailView, LoginRequiredMixin):
    model = Unit
    fields = [
        "name",
        "duration",
        "lessons",
        "created_by",
    ]
    template_name = "courses/unit_detail.html"


class UnitUpdateView(
    SuccessMessageMixin, UpdateView, LoginRequiredMixin, UserPassesTestMixin
):
    model = Unit
    template_name = "courses/unit_update.html"
    success_message = "Unit Updated"
    success_url = reverse_lazy("courses:my-units")

    def test_func(self):
        return self.request.user.is_staff

    def get_form(self, form_class=UnitForm):
        form = super().get_form(form_class)
        form.fields["lessons"].queryset = Lesson.objects.filter(
            created_by=self.request.user
        )
        return form


class UnitDeleteView(
    SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, DeleteView
):
    model = Unit
    template_name = "courses/unit_delete.html"
    success_message = "Unit Deleted"
    success_url = reverse_lazy("courses:my-units")

    def test_func(self):
        return self.request.user.is_staff
