from django.contrib import admin
from .models import PaymeTransaction

# Register your models here.

@admin.register(PaymeTransaction)
class PaymeTransactionAdmin(admin.ModelAdmin):
    readonly_fields = ("record_id", "transaction_id", "amount", "creation_time", "perform_time", "state", "denial_reason", "phone")
