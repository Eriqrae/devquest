from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from django.conf import settings

from reports.models import Report
from reports.forms import ReportForm, ReportResponseForm
from courses.decorators import teacher_required

User = get_user_model()


@login_required
def myreports(request):
    reports = Report.objects.filter(student=request.user)
    return render(request, "reports/myreports.html", {"reports": reports})


@login_required
def create_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report_entry = form.save(commit=False)
            report_entry.student = request.user
            report_entry.save()
            messages.success(request, "Report successfully created")
            return redirect("users:dashboard")
    else:
        form = ReportForm()
    return render(request, "reports/report_entry_form.html", {"form": form})


@login_required
def edit_report(request):
    report = get_object_or_404(Report, student=request.user)
    if request.method == "POST":
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(report, "Report updated successfully")
            return redirect("reports:myreports")
    else:
        form = ReportForm(instance=report)
    return render(request, "reports/report_entry_form.html", {"form": form})


@login_required
@teacher_required
def teacher_view_log_entries(request, student_id):
    student = get_object_or_404(User, id=student_id)
    log_entries = Report.objects.filter(student=student)
    return render(
        request,
        "reports/teacher_report_entries.html",
        {"student": student, "log_entries": log_entries},
    )


@login_required
@teacher_required
def update_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)

    if request.method == "POST":
        form = ReportResponseForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            # return redirect("users:dashboard", student_id=report.student.id)
            messages.success(request, "Solution added successfully")
            return redirect("reports:log-reports")
    else:
        form = ReportResponseForm()

    return render(
        request, "reports/report_entry_update.html", {"report": report, "form": form}
    )


@login_required
@teacher_required
def teacher_log_reports(request):
    # User = settings.AUTH_USER_MODEL
    try:
        students = User.objects.all().prefetch_related(
            Prefetch("log_entries", queryset=Report.objects.order_by("-created_at"))
        )
    except User.DoesNotExist:
        students = []
    return render(request, "reports/reports.html", {"students": students})


# def report_list(request):
#     students = User.objects.all()
#     reports = Report.objects.filter(student=students).order_by("-created_at")

#     return render(
#         request, "reports/reports.html", {"students": students, "reports": reports}
#     )

# def report_list(request):
#     students = User.objects.all()
#     reports = {}

#     for student in students:
#         student_reports = Report.objects.filter(student=student).order_by("-created_at")
#         reports[student] = student_reports

#     return render(request, "reports/reports.html", {"students": students, "reports": reports})

# def report_list(request):
#     students = User.objects.all()

#     return render(
#         request, "reports/reports.html", {"students": students}
#     )


def report_list(request):
    students = User.objects.filter(is_student=True).prefetch_related(
        Prefetch("report_set", queryset=Report.objects.order_by("-created_at"))
    )

    return render(
        request, "reports/reports.html", {"students": students}
    )