from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import now

from tasks.models import Task, TaskSubmission
from courses.decorators import student_required, teacher_required
from tasks.forms import TaskSubmissionForm, TaskForm


@login_required
def task_list(request):
    tasks = Task.objects.all()
    student = request.user

    task_submissions = TaskSubmission.objects.filter(student=student)
    submitted_tasks = [submission.task for submission in task_submissions]

    context = {
        "tasks": tasks,
        "submitted_tasks": submitted_tasks,
        "now": now(),
    }

    return render(request, "tasks/task_list.html", context)


@login_required
@teacher_required
def mytasks(request):
    tasks = Task.objects.filter(created_by=request.user)
    return render(request, "tasks/mytasks.html", {"tasks": tasks})


class TaskCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_create.html"
    success_message = "Task Created"
    success_url = reverse_lazy("tasks:mytasks")

    def form_valid(self, form):
        deadline = form.cleaned_data.get("deadline")
        if deadline and deadline < timezone.now():
            form.add_error("deadline", "The deadline cannot be a past date.")
            return self.form_invalid(form)

        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_update.html"
    success_message = "Task Updated"
    success_url = reverse_lazy("tasks:mytasks")

    def test_func(self):
        return self.request.user.is_staff


@login_required
@student_required
def task_submission_create(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Check if the current user has already submitted the task
    if TaskSubmission.objects.filter(task=task, student=request.user).exists():
        messages.error(request, "You have already submitted this task.")
        return redirect("tasks:task-list")

    # Check if the task is past the deadline
    if task.deadline and task.deadline < timezone.now():
        messages.error(request, "The task submission deadline has passed.")
        return redirect("tasks:task-list")

    if request.method == "POST":
        form = TaskSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.task = task
            submission.student = request.user
            submission.save()

            # Update the task status to "submitted"
            task.status = "submitted"
            task.save()

            messages.success(request, "Task submitted successfully.")
            return redirect("tasks:task-list")

    else:
        form = TaskSubmissionForm()

    context = {
        "task": task,
        "form": form,
    }

    return render(request, "tasks/task_submission_create.html", context)


class TaskSubmissionListView(LoginRequiredMixin, ListView):
    model = TaskSubmission
    template_name = "tasks/task_submission_list.html"
    context_object_name = "submissions"

    def get_queryset(self):
        # Only fetch the task submissions for the tasks created by the logged-in teacher
        return TaskSubmission.objects.filter(task__created_by=self.request.user)


class TaskSubmissionDetailView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = TaskSubmission
    fields = [
        "is_approved",
    ]
    template_name = "tasks/submission_detail.html"
    context_object_name = "submission"
    success_message = "Submission Approved"
    success_url = reverse_lazy("tasks:task-submission-list")

    def get_queryset(self):
        # Only fetch the task submissions for the tasks created by the logged-in teacher
        return TaskSubmission.objects.filter(task__created_by=self.request.user)
