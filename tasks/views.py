from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from tasks.models import Task, TaskSubmission
from courses.decorators import student_required
from tasks.forms import TaskSubmissionForm


@login_required
def task_list(request):
    tasks = Task.objects.all()
    student = request.user

    task_submissions = TaskSubmission.objects.filter(student=student)
    submitted_tasks = [submission.task for submission in task_submissions]

    context = {"tasks": tasks, "submitted_tasks": submitted_tasks}

    return render(request, "tasks/task_list.html", context)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/mytasks.html"
    context_object_name = "tasks"


class TaskCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Task
    fields = [
        "title",
        "description",
        "document",
        "task_link",
    ]
    template_name = "tasks/task_create.html"
    success_message = "Task Created"
    success_url = reverse_lazy("tasks:task-list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


class TaskSubmissionCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = TaskSubmission
    fields = [
        "document",
        "answer",
    ]
    template_name = "tasks/task_submission_create.html"
    success_message = "Task submitted"
    success_url = reverse_lazy("tasks:task-list")

    def form_valid(self, form):
        task = Task.objects.get(pk=self.kwargs["pk"])
        form.instance.task = task
        form.instance.student = self.request.user
        task.status = "submitted"
        task.save()
        return super().form_valid(form)


@login_required
@student_required
def task_submission_create(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Check if the current user has already submitted the task
    if TaskSubmission.objects.filter(task=task, student=request.user).exists():
        messages.error(request, "You have already submitted this task.")
        return redirect("tasks:task-list")

    form = TaskSubmissionForm(request.POST or None)

    if request.method == "POST":
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

    context = {
        "task": task,
        "form": form,
    }

    return render(request, "tasks/task_submission_create.html", context)


# class TaskSubmissionApproveView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
#     model = TaskSubmission
#     template_name = "tasks/task_submission_approve.html"
#     context_object_name = "submission"

#     def test_func(self):
#         return self.request.user == self.get_object().task.created_by

#     def get_success_url(self):
#         return "tasks:tasks"

#     def approve_submission(self):
#         submission = self.get_object()
#         submission.is_approved = True
#         submission.task.status = "approved"
#         submission.task.save()
#         submission.save()
#         return redirect(self.get_success_url())

#     def disapprove_submission(self):
#         submission = self.get_object()
#         submission.is_approved = False
#         submission.task.status = "disapproved"
#         submission.task.save()
#         submission.save()
#         return redirect(self.get_success_url())


class TaskSubmissionListView(ListView):
    model = TaskSubmission
    template_name = "tasks/task_submission_list.html"
    context_object_name = "submissions"

    def get_queryset(self):
        # Only fetch the task submissions for the tasks created by the logged-in teacher
        return TaskSubmission.objects.filter(task__created_by=self.request.user)


# class TaskSubmissionApproveView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
#     model = TaskSubmission
#     template_name = "tasks/task_submission_approve.html"
#     context_object_name = "submission"

#     def test_func(self):
#         return self.request.user == self.get_object().task.created_by

#     def get_success_url(self):
#         return "tasks:task-list"

#     def post(self, request, *args, **kwargs):
#         submission = self.get_object()
#         action = request.POST.get("action")

#         if action == "approve":
#             self.approve_submission(submission)
#         elif action == "disapprove":
#             self.disapprove_submission(submission)

#         return redirect(self.get_success_url())

#     def approve_submission(self, submission):
#         submission.is_approved = True
#         submission.task.status = "approved"
#         submission.task.save()
#         submission.save()

#     def disapprove_submission(self, submission):
#         submission.is_approved = False
#         submission.task.status = "disapproved"
#         submission.task.save()
#         submission.save()


class TaskSubmissionApproveView(DetailView):
    model = TaskSubmission
    template_name = "task/task_submission_approve.html"
    context_object_name = "submission"

    def post(self, request, pk):
        submission = get_object_or_404(TaskSubmission, pk=pk)
        action = request.POST.get("action")

        if action == "approve":
            self.approve_submission(submission)
        elif action == "disapprove":
            self.disapprove_submission(submission)

        return redirect("tasks:task-submission-list")

    def approve_submission(self, submission):
        submission.status = "approved"
        submission.save()

    def disapprove_submission(self, submission):
        submission.status = "disapproved"
        submission.save()
