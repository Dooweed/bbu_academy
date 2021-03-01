from django.urls import path
from . import views

app_name = "payme-billing"

urlpatterns = [
    path("", views.payme_billing, name="endpoint"),
]
