from django.contrib import admin

from urllib.parse import quote
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.safestring import mark_safe

from .forms import CertificateAdminForm, MultiCertificateAdminForm
from .models import Certificate
from tools.colorsets import SUCCESS_COLORS, COMMON_COLORS


from .utils import build_certificate_excel


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("full_name", "inn_or_pinfl", "certificate_n", "date_received")
    list_filter = ("date_received",)
    search_fields = ("pinfl", "inn", "certificate_n", "contract_n", "full_name", "date_received")
    fields = ("contract_n", "certificate_n", "pinfl", "inn", "full_name", "date_received")
    actions = ("download_excel", )
    list_max_show_all = 5000

    form = CertificateAdminForm

    def download_excel(self, request, queryset):
        file = build_certificate_excel(queryset)
        file.name = "Сертификаты.xls"
        response = HttpResponse(file.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f"""attachment; filename="certificates.xls"; filename*=utf-8''{quote("Сертификаты.xls")}"""
        return response
    download_excel.short_description = "Скачать выбранные сертификаты в Excel файле"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('add_multiple/', self.admin_site.admin_view(self.multiple_certificate_view), name="add_multiple"),
        ]
        return my_urls + urls

    def multiple_certificate_view(self, request):
        context = dict(
            self.admin_site.each_context(request),
            opts=self.opts,
            add=True,
            change=False,
            save_as=self.save_as,
            has_add_permission=self.has_add_permission,
            has_change_permission=self.has_change_permission,
            has_view_permission=self.has_view_permission,
            has_delete_permission=self.has_delete_permission,
            has_editable_inline_admin_formsets=False,
            has_file_field=True,
            show_save=True,
            show_save_and_continue=False,
            show_save_and_add_another=False,
            title="Загрузить файл с сертификатами",
        )

        if request.method == "POST":
            form = MultiCertificateAdminForm(request.POST, request.FILES)
            if form.is_valid():
                created, renewed, skipped, incorrect, report = form.save_certificates()
                context['colors'] = SUCCESS_COLORS
                context['help_text'] = f"""<b>Загрузка прошла успешно.</b><br>
                                           <span style="margin-left: 10px">Создано записей: <b>{created}</b></span>
                                           <span style="margin-left: 20px">Обновлено записей: <b>{renewed}</b></span>
                                           <span style="margin-left: 20px">Пропущено записей: <b>{skipped}</b></span>
                                           <span style="color: red; margin-left: 20px">Неверных сертификатов: <b>{incorrect}</b></span>
                                           <span style="margin-left: 20px; text-decoration: underline;">Всего сертификатов: <b>{created+renewed+skipped+incorrect}</b></span>"""
                if incorrect > 0:
                    context['report'] = report
                form = MultiCertificateAdminForm()
            else:
                context['colors'] = COMMON_COLORS
                context['help_text'] = f"""Загрузка новых сертификатов может занять некоторое время"""

        else:
            form = MultiCertificateAdminForm()
            context['colors'] = COMMON_COLORS
            context['help_text'] = f"""Загрузка новых сертификатов может занять некоторое время"""

        context['form'] = form
        return TemplateResponse(request, "admin/certificates/multi-certificate-form.html", context)

    def inn_or_pinfl(self, obj):
        return mark_safe(f'<span style="color:gray">ИНН</span>: {obj.inn}' if obj.inn else f'<span style="color:gray">ПИНФЛ</span>: {obj.pinfl}')
    inn_or_pinfl.short_description = "ИНН или ПИНФЛ"
