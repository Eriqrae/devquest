from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import Teacher

CustomUser = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
        )


class TeacherCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_staff = True
        user.is_teacher = True
        user.save()
        Teacher.objects.create(user=user)
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
        )
