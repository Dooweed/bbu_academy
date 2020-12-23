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
            "meta_description": forms.Textarea(attrs={"style": "width: 400px; height: 68px;"}),
        }


@admin.register(Training)
class TrainingAdmin(SortableAdminMixin, ImageCroppingMixin, TranslationAdmin):
    list_display = ("title", "url", "short_text", "sorting")
    search_fields = ("title", "short_text", "location", "text")
    fieldsets = (
        (None, {"fields": ("title", "url", "active")}),
        ("Описание", {"fields": ("text", "short_text", "meta_description")}),
        ("Изображение", {"fields": ("image", "sidebar_size", "thumbnail_size")}),
    )
    prepopulated_fields = {'url': ('title',), }
    form = TrainingForm
