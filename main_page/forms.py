from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms.utils import ErrorList


class MainSliderForm(forms.ModelForm):
    def clean(self):
        reference_name = self.cleaned_data.get('reference')
        reference = self.cleaned_data.get(reference_name)
        if reference is None:
            if reference_name not in self._errors:
                self._errors[reference_name] = ErrorList()
            self._errors[reference_name].append('Выберите запись из списка')

        return self.cleaned_data

    class Meta:
        fields = ("title", "text", "reference", "news_reference", "training_reference", "course_reference", "button")
        widgets = {
            "reference": forms.RadioSelect(),
            "button": forms.RadioSelect(),
            'text': CKEditorWidget(),
            'title': forms.Textarea(attrs={"style": "width: 400px; height: 34px;"}),
        }


class SecondarySliderForm(forms.ModelForm):
    def clean(self):
        reference_name = self.cleaned_data.get('reference')
        reference = self.cleaned_data.get(reference_name)
        if reference is None:
            if reference_name not in self._errors:
                self._errors[reference_name] = ErrorList()
            self._errors[reference_name].append('Выберите запись из списка')

        return self.cleaned_data

    class Meta:
        fields = ("title", "text", "reference", "news_reference", "training_reference", "course_reference")
        widgets = {
            "reference": forms.RadioSelect(),
            'text': CKEditorWidget(),
            'title': forms.Textarea(attrs={"style": "width: 400px; height: 34px;"}),
        }


class SingleBlockForm(forms.ModelForm):
    def clean(self):
        reference_name = self.cleaned_data.get('reference')
        reference = self.cleaned_data.get(reference_name)
        if reference is None:
            if reference_name not in self._errors:
                self._errors[reference_name] = ErrorList()
            self._errors[reference_name].append('Выберите запись из списка')

        return self.cleaned_data

    class Meta:
        fields = ("title", "text", "reference", "news_reference", "training_reference", "course_reference")
        widgets = {
            "reference": forms.RadioSelect(),
            'text': CKEditorWidget(),
            'title': forms.Textarea(attrs={"style": "width: 400px; height: 34px;"}),
        }


class StaticBlockForm(forms.ModelForm):
    def clean(self):
        reference_name = self.cleaned_data.get('reference')
        reference = self.cleaned_data.get(reference_name)
        if reference is None:
            if reference_name not in self._errors:
                self._errors[reference_name] = ErrorList()
            self._errors[reference_name].append('Выберите запись из списка')

        return self.cleaned_data

    class Meta:
        fields = ("title", "text", "reference", "news_reference", "training_reference", "course_reference")
        widgets = {
            "reference": forms.RadioSelect(),
            'text': CKEditorWidget(),
            'title': forms.Textarea(attrs={"style": "width: 400px; height: 34px;"}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        widgets = {
            'text': forms.Textarea(attrs={"style": "width: 400px; height: 136px;"}),
        }