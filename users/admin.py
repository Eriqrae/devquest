from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Teacher, Student, Supervisor

CustomUser = get_user_model()

admin.site.register(CustomUser)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Supervisor)


# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = (
#         "email",
#         "first_name",
#         "last_name",
#         "is_staff",
#         "is_active",
#     )
#     list_filter = (
#         "email",
#         "first_name",
#         "last_name",
#         "is_staff",
#         "is_active",
#     )
#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         (
#             "Permissions",
#             {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
#         ),
#     )
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": (
#                     "email",
#                     "password1",
#                     "password2",
#                     "is_staff",
#                     "is_active",
#                     "groups",
#                     "user_permissions",
#                 ),
#             },
#         ),
#     )
#     search_fields = ("email",)
#     ordering = ("email",)


# admin.site.register(CustomUser, CustomUserAdmin)
