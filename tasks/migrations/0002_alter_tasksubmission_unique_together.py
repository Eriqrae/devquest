# Generated by Django 4.2.2 on 2023-06-18 22:30

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="tasksubmission",
            unique_together={("task", "student")},
        ),
    ]
