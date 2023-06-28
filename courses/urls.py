from django.urls import path

from courses.views import (
    UnitListView,
    UnitDetailView,
    UnitUpdateView,
    UnitDeleteView,
    unit_page,
    add_resource,
    myresources,
    mylessons,
    ResourceDetailView,
    ResourcesDeleteView,
    ResourcesListView,
    ResourcesUpdateView,
    LessonCreateView,
    LessonListView,
    LessonDetailView,
    LessonDeleteView,
    LessonUpdateView,
    UnitCreateView,
)

app_name = "courses"

urlpatterns = [
    path("myunits/", unit_page, name="my-units"),
    path("unit/", UnitCreateView.as_view(), name="unit-create"),
    path("units/", UnitListView.as_view(), name="unit-list"),
    path("unit/<str:pk>/", UnitDetailView.as_view(), name="unit-detail"),
    path("unit/<str:pk>/update/", UnitUpdateView.as_view(), name="unit-update"),
    path("unit/<str:pk>/delete/", UnitDeleteView.as_view(), name="unit-delete"),
    # Resources urls
    path("myresources/", myresources, name="myresources"),
    path("resource/", add_resource, name="resources-create"),
    path("resources/", ResourcesListView.as_view(), name="resources-list"),
    path("resources/<str:pk>/", ResourceDetailView.as_view(), name="resources-detail"),
    path(
        "resources/<str:pk>/update/",
        ResourcesUpdateView.as_view(),
        name="resources-update",
    ),
    path(
        "resources/<str:pk>/delete/",
        ResourcesDeleteView.as_view(),
        name="resources-delete",
    ),
    # lessons urls
    path("mylessons/", mylessons, name="mylessons"),
    path("lesson/", LessonCreateView.as_view(), name="lessons-create"),
    path("lessons/", LessonListView.as_view(), name="lessons-list"),
    path("lesson/<str:pk>/", LessonDetailView.as_view(), name="lessons-detail"),
    path("lesson/<str:pk>/update/", LessonUpdateView.as_view(), name="lessons-update"),
    path("lesson/<str:pk>/delete/", LessonDeleteView.as_view(), name="lessons-delete"),
]
