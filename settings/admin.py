from django.contrib import admin
from .models import Page, StaticInformation
from modeltranslation.admin import TranslationAdmin
from adminsortable2.admin import SortableAdminMixin

# Register your models here.

@admin.register(Page)
class PageAdmin(SortableAdminMixin, TranslationAdmin):
    list_display = ("title", "name", "show_in_menu", "sorting")
    fieldsets = (
        ("Главная информация", {'fields': ("name", "title", "template_name", "parent_page", "show_in_menu", "menu_name")}),
        ("Мета-теги (Поисковая оптимизация)", {'fields': ("meta_description", "meta_keywords", "meta_robots")})
    )

@admin.register(StaticInformation)
class StaticInformationAdmin(admin.ModelAdmin):
    list_display = ("name", "value", "key")

    readonly_fields = ("name", "key")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
