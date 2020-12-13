from django import forms

class MessageForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control", "id": "contactform-name", "name": "ContactForm[name]"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control", "id": "contactform-email", "name": "ContactForm[email]"}))
    subject = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control", "id": "contactform-subject", "name": "ContactForm[subject]"}))
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form-control", "id": "contactform-body", "name": "ContactForm[body]", "cols": 6}))
