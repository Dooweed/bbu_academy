from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.urls import reverse, NoReverseMatch

from .models import Page, StaticInformation
from modeltranslation.admin import TranslationAdmin
from adminsortable2.admin import SortableAdminMixin

# Register your models here.

admin.site.site_header = "ATБ - Админ панель"

class PageAdminForm(ModelForm):
    def clean(self):
        name = self.instance.name
        show_in_menu = self.cleaned_data.get("show_in_menu")
        if show_in_menu:
            try:
                reverse(name)
            except NoReverseMatch:
                raise ValidationError({"show_in_menu": "Невозможно добавить в меню. Имя страницы не зарегестрировано в urls.py."})


@admin.register(Page)
class PageAdmin(SortableAdminMixin, TranslationAdmin):
    list_display = ("title", "name", "show_in_menu", "sorting")
    fieldsets = (
        ("Главная информация", {'fields': ("title", "menu_name", "show_in_menu", "parent_page", "name", "template_name")}),
        ("Мета-теги (Поисковая оптимизация)", {'fields': ("meta_description", "meta_keywords", "meta_robots")})
    )
    readonly_fields = ("name", "template_name")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    form = PageAdminForm

@admin.register(StaticInformation)
class StaticInformationAdmin(admin.ModelAdmin):
    list_display = ("name", "value", "key")
    list_editable = ("value", )

    readonly_fields = ("name", "key")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
