from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Teacher, Student, Supervisor

CustomUser = get_user_model()

admin.site.register(CustomUser)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Supervisor)
