from datetime import datetime

from django.contrib import admin
from django.http import HttpResponse
from urllib.parse import quote

from tools.utils import model_to_excel
from .models import *

# Register your models here.

class IndividualPayerInline(admin.StackedInline):
    model = IndividualPayer
    extra = 0
    can_delete = False

    class Media:
        css = {'all': ('css/no-add_another-button.css',)}

class EntityPayerInline(admin.StackedInline):
    model = EntityPayer
    extra = 0
    can_delete = False

    class Media:
        css = {'all': ('css/no-add_another-button.css',)}


@admin.register(SmallPurchaseRecord)
class SmallPurchaseRecordAdmin(admin.ModelAdmin):
    list_filter = ("is_paid", "finished", "overall_price", "payment_type", "date_started", "date_finished")
    list_display = ("invoice_n", "product", "payer_name", "payer_type", "overall_price", "payment_type", "date_started", "finished")

    # "id", "finished", "study_type", "payment_type", "get_price", "overall_price", "date_started", "date_finished"
    fields = ("id", "admin_invoice_link", "state", "offer_agreement", "amount", "is_paid", "finished", "special_price", "payment_type", "price",
              "overall_price", "date_started", "date_finished")
    readonly_fields = ("id", "admin_invoice_link", "price", "date_started", "date_finished", "overall_price")
    inlines = (IndividualPayerInline, EntityPayerInline)

    actions = ("download_excel", )
    save_on_top = True

    def download_excel(self, request, queryset):
        fields = ("id", "payer_type", "payer_name", "get_payment_type_display", "price", "overall_price", "date_started", "date_finished", "offer_agreement",
                  "special_price", "is_paid", "finished")
        file = model_to_excel(queryset, fields)
        file.name = f"Покупки-({datetime.now()}).xls"
        response = HttpResponse(file.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f"""attachment; filename="certificates.xls"; filename*=utf-8''{quote(file.name)}"""
        return response
    download_excel.short_description = "Скачать выбранные покупки в Excel файле"

    def get_inlines(self, request, obj):
        if obj.payer:
            return (eval(f"{type(obj.payer).__name__}Inline"),)
        else:
            return tuple()

    def has_add_permission(self, request):
        return False
