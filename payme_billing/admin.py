from django.contrib import admin
from .models import PaymeTransaction

# Register your models here.

@admin.register(PaymeTransaction)
class PaymeTransactionAdmin(admin.ModelAdmin):
    readonly_fields = super().fields
