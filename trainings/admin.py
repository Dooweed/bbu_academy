from adminsortable2.admin import SortableAdminMixin
from ckeditor.widgets import CKEditorWidget
from django.contrib import admin

# Register your models here.
from django import forms
from image_cropping import ImageCroppingMixin
from modeltranslation.admin import TranslationAdmin

from .models import Training

class TrainingForm(forms.ModelForm):
    class Meta:
        fields = ("title", "url", "active", "image", "sidebar_size", "thumbnail_size", "price", "short_text", "meta_description", "text")
        widgets = {
            'title': forms.Textarea(attrs={"style": "width: 400px; height: 68px;"}),
            'url': forms.Textarea(attrs={"style": "width: 400px; height: 34px;"}),
            # 'location': forms.Textarea(attrs={"style": "width: 400px; height: 34px;"}),
            'short_text': forms.Textarea(attrs={"style": "width: 400px; height: 68px;"}),
            'text': CKEditorWidget(),
            'price': forms.NumberInput(),
            'special_price': forms.NumberInput(),
            "meta_description": forms.Textarea(attrs={"style": "width: 400px; height: 68px;"}),
        }


@admin.register(Training)
class TrainingAdmin(SortableAdminMixin, ImageCroppingMixin, TranslationAdmin):
    list_display = ("title", "url", "short_text", "sorting")
    search_fields = ("title", "short_text", "location", "text")
    fieldsets = (
        ("Заголовок", {"fields": ("title",), "classes": ("visual-group",)}),
        (None, {"fields": ("url", "active", "price", "special_price")}),
        ("Изображение", {"fields": ("image", "sidebar_size", "thumbnail_size"), "classes": ("visual-group", "wide",)}),
        ("Текст", {"fields": ("text",), "classes": ("visual-group", "wide",)}),
        ("Краткое описание", {"fields": ("short_text",), "classes": ("visual-group",)}),
        ("Мета-теги (Описание)", {"fields": ("meta_description",), "classes": ("visual-group",)}),
    )
    prepopulated_fields = {'url': ('title',), }
    form = TrainingForm

    class Media:
        css = {
            "all": ("css/admin-visual-grouping.css", ),
        }
