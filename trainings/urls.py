from django.urls import path
from . import views

app_name = "trainings"

urlpatterns = [
    path("<str:training_url>/", views.training_view, name="training"),
    path("", views.trainings_list_view, name="trainings"),
]
