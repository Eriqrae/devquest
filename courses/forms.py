from django import forms
from courses.models import Unit, Resources, Lesson


class ResourcesForm(forms.ModelForm):
    class Meta:
        model = Resources
        fields = (
            "name",
            "link_one",
            "link_two",
            "link_three",
            "course_notes",
        )


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = (
            "topic",
            "objectives",
            "resources",
        )
        widgets = {"resources": forms.CheckboxSelectMultiple()}


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = (
            "name",
            "duration",
            "lessons",
        )
        widgets = {"lessons": forms.CheckboxSelectMultiple()}
