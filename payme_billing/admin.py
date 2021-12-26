from django.contrib import admin
from .models import PaymeTransaction
from .vars.settings import ADMIN


if ADMIN:
    @admin.register(PaymeTransaction)
    class PaymeTransactionAdmin(admin.ModelAdmin):
        list_display = ("transaction_id", "record_id", "phone")
        list_filter = ("state",)
        search_fields = ("transaction_id", "record_id")
        fields = ("transaction_id", "state", "record_id", "phone", "amount", "payme_creation_time", "creation_time", "perform_time", "cancel_time", "denial_reason")
        readonly_fields = ("record_id", "transaction_id", "amount", "creation_time", "perform_time", "cancel_time", "payme_creation_time", "denial_reason", "phone")
