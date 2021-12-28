from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from purchase.utils import validate_file_2mb
from small_purchase.models import IndividualPayer, EntityPayer, SmallPurchaseRecord

YEARS = [i for i in reversed(range(1900, timezone.now().year + 1))]

class IndividualPayerForm(forms.ModelForm):
    passport = forms.ImageField(label=_("Скан-копия паспорта"), validators=(validate_file_2mb, ), help_text=_('Размер файла до 2Мб'))

    def clean(self):
        # Validate inn
        pinfl = self.cleaned_data.get("pinfl")
        if not pinfl or len(pinfl) != 14:
            raise ValidationError({"pinfl": [_("ПИНФЛ должен состоять из 14 цифр"), ]})
        return self.cleaned_data

    class Meta:
        fields = ("full_name", "pinfl", "passport_n", "phone_number", "email", "telegram_contact")
        model = IndividualPayer
        widgets = {'pinfl': forms.NumberInput(attrs={"class": "hide-arrows"})}


class EntityPayerForm(forms.ModelForm):
    def clean(self):
        # Validate inn
        inn = self.cleaned_data.get("org_inn")
        if not inn or len(inn) != 9:
            raise ValidationError({"org_inn": [_("ИНН должен состоять из 9 цифр"), ]})
        return self.cleaned_data

    class Meta:
        fields = ("org_name", "address", "phone_number", "org_inn", "email", "head_name")
        model = EntityPayer
        widgets = {'org_inn': forms.NumberInput(attrs={"class": "hide-arrows"})}


class ConfirmationForm(forms.ModelForm):
    class Meta:
        model = SmallPurchaseRecord
        fields = ("service", "amount", "special_price")

class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["payment_type"].required = True
        if kwargs.get("instance"):
            self.fields["payment_type"].choices = kwargs.get("instance").get_payment_type_choices()

    class Meta:
        model = SmallPurchaseRecord
        fields = ("payment_type", )
