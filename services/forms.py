from ckeditor.widgets import CKEditorWidget
from django import forms


class ServiceAdminForm(forms.ModelForm):
    class Meta:
        fields = ("title", "url", "active", "image", "sidebar_size", "thumbnail_size", "price", "short_text", "meta_description", "text")
        widgets = {
            'title': forms.Textarea(attrs={"style": "width: 400px; height: 68px;"}),
            'url': forms.Textarea(attrs={"style": "width: 400px; height: 34px;"}),
            'short_text': forms.Textarea(attrs={"style": "width: 400px; height: 68px;"}),
            'text': CKEditorWidget(),
            'price': forms.NumberInput(),
            'special_price': forms.NumberInput(),
            "meta_description": forms.Textarea(attrs={"style": "width: 400px; height: 68px;"}),
        }