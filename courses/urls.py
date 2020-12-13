from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("<str:course_url>/", views.course_view, name="course"),
    path("", views.courses_list_view, name="courses"),
]
