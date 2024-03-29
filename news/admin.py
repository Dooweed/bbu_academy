from django.contrib import admin
from django import forms
from django.contrib import messages
from django.utils.translation import ngettext
from image_cropping import ImageCroppingMixin
from ckeditor.widgets import CKEditorWidget
from modeltranslation.admin import TranslationAdmin

from .models import *


# Register your models here.

class ArticleForm(forms.ModelForm):
    class Meta:
        fields = ("title", "url", "category", "short_text", "meta_description", "status", "date", "text", "image", "thumbnail_size")
        widgets = {
            'title': forms.Textarea(attrs={"style": "width: 400px; height: 34px;"}),
            'url': forms.Textarea(attrs={"style": "width: 400px; height: 34px;"}),
            'short_text': forms.Textarea(attrs={"style": "width: 400px; height: 68px;"}),
            'text': CKEditorWidget(),
            "meta_description": forms.Textarea(attrs={"style": "width: 400px; height: 68px;"}),
        }
        model = Article


@admin.register(Article)
class ArticleAdmin(ImageCroppingMixin, TranslationAdmin):
    list_display = ("title", "status", "url", "has_image", "date", "short_text", "category")
    search_fields = ("title", "short_text", "text")
    list_editable = ("status",)
    actions = ("make_published", 'make_pending', 'make_editing')
    prepopulated_fields = {'url': ('title',), }

    fieldsets = (
        ("Заголовок", {"fields": ("title",), "classes": ("visual-group",)}),
        (None, {"fields": ("url", "category", "status", "date")}),
        ("Изображение", {"fields": ("image", "thumbnail_size"), "classes": ("visual-group", "wide",)}),
        ("Текст", {"fields": ("text",), "classes": ("visual-group", "wide", )}),
        ("Краткое описание", {"fields": ("short_text",), "classes": ("visual-group",)}),
        ("Мета-теги (Описание)", {"fields": ("meta_description",), "classes": ("visual-group", "collapse")}),
    )

    form = ArticleForm

    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, ngettext(
            '%d статья была успешно опубликована.',
            '%d статей были успешно опубликованы.',
            updated,
        ) % updated, messages.SUCCESS)

    make_published.short_description = "Опубликовать"

    def make_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, ngettext(
            '%d статья была успешно переведена в режим ожидания.',
            '%d статей были успешно переведены в режим ожидания.',
            updated,
        ) % updated, messages.SUCCESS)

    make_pending.short_description = "Перевести в режим ожидания"

    def make_editing(self, request, queryset):
        updated = queryset.update(status='editing')
        self.message_user(request, ngettext(
            '%d статья была успешно переведена в режим редактирования.',
            '%d статей были успешно переведены в режим редактирования.',
            updated,
        ) % updated, messages.SUCCESS)

    make_editing.short_description = "Перевести в режим редактирования"

    class Media:
        css = {
            "all": ("css/admin-visual-grouping.css", ),
        }


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
