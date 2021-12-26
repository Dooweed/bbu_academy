from django.urls import path
from . import views

app_name = "small_purchase"

urlpatterns = [
    path("offer-agreement/", views.offer_agreement_view, name="offer-agreement"),
    path("form/individual/", views.individual_form_view, name="individual-form"),
    path("form/entity/", views.entity_form_view, name="entity-form"),
    path("form/confirmation/", views.confirmation_form_view, name="confirmation-form"),
    path("form/payment/", views.payment_form_view, name="payment-form"),
    path("form/payme/", views.payme_payment_view, name="payme-payment"),
    path("form/finished/", views.payment_finished_view, name="finished"),
]
