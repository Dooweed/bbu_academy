from django.contrib import admin

from .models import Page, StaticInformation
from modeltranslation.admin import TranslationAdmin
from adminsortable2.admin import SortableAdminMixin

admin.site.site_header = "ATБ - Админ панель"


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


@admin.register(StaticInformation)
class StaticInformationAdmin(admin.ModelAdmin):
    list_display = ("name", "value", "key")
    list_editable = ("value", )

    readonly_fields = ("name", "key")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
