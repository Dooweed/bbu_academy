from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    path("<str:service_url>/", views.service_view, name="service"),
    path("", views.services_list_view, name="services"),
]
