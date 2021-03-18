from abc import abstractmethod

from django import forms
from django.template.loader import render_to_string

from .vars.settings import WEB_CASH_ID


class BasePaymentInitialisationForm(forms.Form):
    merchant = forms.CharField(widget=forms.HiddenInput)
    purchase_id = forms.IntegerField(widget=forms.HiddenInput())
    phone = forms.CharField(widget=forms.HiddenInput(), max_length=9, min_length=9)
    amount = forms.IntegerField(widget=forms.HiddenInput)
    lang = forms.CharField(widget=forms.HiddenInput, max_length=2, min_length=2)

    def __init__(self, purchase_id, phone, amount, lang, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["merchant"].initial = WEB_CASH_ID
        self.fields["purchase_id"].initial = purchase_id
        self.fields["phone"].initial = phone
        self.fields["amount"].initial = amount
        self.fields["lang"].initial = lang
        self.fields["callback"].initial = callback

    def add_prefix(self, field_name):
        FIELD_NAME_MAPPING = {
            "purchase_id": 'account[purchase_id]',
            "phone": 'account[phone]',
        }
        field_name = FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(BasePaymentInitialisationForm, self).add_prefix(field_name)

    @abstractmethod
    def render(self):
        pass


class ButtonBasePaymentInitialisationForm(BasePaymentInitialisationForm):
    button = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, purchase_id, phone, amount, lang, callback=None, type="svg", style="colored", width=200, *args, **kwargs):
        # Check type argument
        available_types = ("svg", "png")
        if type not in available_types:
            raise ValueError(f"type argument must be one of {available_types}")

        # Check style argument
        available_styles = ("colored", "white")
        if style not in available_styles:
            raise ValueError(f"style argument must be one of {available_styles}")

        # Check width argument
        if not isinstance(width, int) and not isinstance(width, float):
            raise ValueError(f"width argument must be integer or float")

        super().__init__(purchase_id, phone, amount, lang, callback, *args, **kwargs)

        self.fields["button"].widget.attrs.update({"data-type": type, "value": style, "data-width": width})

    def render(self):
        return render_to_string("button-form.html", {"form": self})


class QrBasePaymentInitialisationForm(BasePaymentInitialisationForm):
    qr = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, purchase_id, phone, amount, lang, callback=None, size=250, *args, **kwargs):
        # Check width argument
        if not isinstance(size, int) and not isinstance(size, float):
            raise ValueError(f"size argument must be integer or float")

        super().__init__(purchase_id, phone, amount, lang, callback, *args, **kwargs)

        self.fields["qr"].widget.attrs["data-width"] = size

    def render(self):
        return render_to_string("qr-form.html", {"form": self})
