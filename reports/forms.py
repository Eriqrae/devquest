from django import forms

from reports.models import Report


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            "activity",
            "problems",
            "solutions",
        ]


class ReportResponseForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            "response",
        ]
