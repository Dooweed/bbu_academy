from django import forms
from django.core.exceptions import ValidationError


class MessageForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control", "id": "contactform-name", "name": "ContactForm[name]"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control", "id": "contactform-email", "name": "ContactForm[email]"}))
    subject = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "id": "contactform-subject", "name": "ContactForm[subject]"}))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form-control", "id": "contactform-body", "name": "ContactForm[body]", "cols": 6}))
    message1 = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control", "id": "contactform-body", "name": "ContactForm[body]", "cols": 6,
                                                                           "style": "opacity: 0; height: 0; padding: 0;"}))

    def clean(self):
        form_data = self.cleaned_data

        if form_data.get('message1', None):
            raise ValidationError('Ваша заявка была определена как спам', code='spam')
        return form_data
