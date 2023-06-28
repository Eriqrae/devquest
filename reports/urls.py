from django.urls import path
from reports.views import (
    myreports,
    create_report,
    edit_report,
    teacher_view_log_entries,
    update_report,
    teacher_log_reports,
    report_list,
)

app_name = "reports"

urlpatterns = [
    path("myreports/", myreports, name="myreports"),
    path("create/", create_report, name="report-create"),
    path("edit/<str:id>/", edit_report, name="edit-report"),
    path("reports/<str:student_id>/", teacher_view_log_entries, name="reports"),
    path("update/<str:report_id>/", update_report, name="report-update"),
    path('log-reports/', report_list, name='log-reports'),
]
