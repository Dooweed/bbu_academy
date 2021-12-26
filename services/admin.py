from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from image_cropping import ImageCroppingMixin
from modeltranslation.admin import TranslationAdmin

from .forms import ServiceAdminForm
from .models import Service


@admin.register(Service)
class ServiceAdmin(SortableAdminMixin, ImageCroppingMixin, TranslationAdmin):
    list_display = ("title", "url", "has_image", "short_text", "price", "sorting")
    search_fields = ("title", "short_text", "text")
    fieldsets = (
        ("Заголовок", {"fields": ("title",), "classes": ("visual-group",)}),
        (None, {"fields": ("url", "active", ("price", "special_price"))}),
        ("Изображение", {"fields": ("image", "sidebar_size", "thumbnail_size"), "classes": ("visual-group", "wide",)}),
        ("Текст", {"fields": ("text",), "classes": ("visual-group", "wide",)}),
        ("Краткое описание", {"fields": ("short_text",), "classes": ("visual-group",)}),
        ("Мета-теги (Описание)", {"fields": ("meta_description",), "classes": ("visual-group", "collapse")}),
    )
    prepopulated_fields = {'url': ('title',), }
    form = ServiceAdminForm

    class Media:
        css = {
            "all": ("css/admin-visual-grouping.css", ),
        }
