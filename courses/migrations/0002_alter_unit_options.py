# Generated by Django 4.2.2 on 2023-06-26 15:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="unit",
            options={"ordering": ["-created_at"]},
        ),
    ]