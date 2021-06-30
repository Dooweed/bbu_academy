from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.functional import lazy

from courses.models import Course
from purchase.models import Student, IndividualPayer, PurchaseRecord, EntityPayer
from purchase.utils import get_product_choices
from .utils import validate_file_2mb
from trainings.models import Training

YEARS = tuple([i for i in range(1900, timezone.now().year)])


class StudentForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    student_passport = forms.ImageField(label=_("Скан-копия паспорта студента"), validators=(validate_file_2mb, ), help_text=_('Размер файла до 2Мб'))
    study_document = forms.ImageField(label=_("Документы об образовании"), validators=(validate_file_2mb, ), help_text=_('Размер файла до 2Мб'))

    def get_student_fields(self):
        return [self[x] for x in self.fields if x.startswith("student_")]

    def get_rest_fields(self):
        return {x: self[x] for x in self.fields if not x.startswith("student_")}

    def id_is_valid(self):
        self.full_clean()
        return self.cleaned_data and 'id' in self.cleaned_data and self.cleaned_data['id'] is not None

    def clean(self):
        # Validate inn
        inn = self.cleaned_data.get("student_inn")
        if not inn or len(inn) != 9:
            raise ValidationError({"student_inn": [_("ИНН должен состоять из 9 цифр"), ]})
        return self.cleaned_data

    class Meta:
        fields = ("student_full_name", "student_inn", "student_passport_n", "student_passport_received_date", "student_passport_given_by", "student_phone_number", "student_email",
                  "student_telegram_contact", "study_type", "study_document", "student_passport")
        model = Student
        widgets = {'student_passport_received_date': forms.SelectDateWidget(years=YEARS, attrs={"class": "datepicker"}),
                   'student_inn': forms.NumberInput(attrs={"class": "hide-arrows"})}


class IndividualPayerForm(forms.ModelForm):
    individual_payer_passport = forms.ImageField(label=_("Скан-копия паспорта плательщика"), validators=(validate_file_2mb, ), help_text=_('Размер файла до 2Мб'))

    def clean(self):
        # Validate inn
        inn = self.cleaned_data.get("individual_payer_inn")
        if not inn or len(inn) != 9:
            raise ValidationError({"individual_payer_inn": [_("ИНН должен состоять из 9 цифр"), ]})
        return self.cleaned_data

    class Meta:
        fields = ("individual_payer_full_name", "individual_payer_inn", "individual_payer_passport_n", "individual_payer_passport_received_date",
                  "individual_payer_passport_given_by", "individual_payer_phone_number", "individual_payer_email", "individual_payer_telegram_contact")
        model = IndividualPayer
        widgets = {'individual_payer_passport_received_date': forms.SelectDateWidget(years=YEARS, attrs={"class": "datepicker"}),
                   'individual_payer_inn': forms.NumberInput(attrs={"class": "hide-arrows"})}


class EntityPayerForm(forms.ModelForm):
    def clean(self):
        # Validate inn
        inn = self.cleaned_data.get("entity_payer_org_inn")
        if not inn or len(inn) != 9:
            raise ValidationError({"entity_payer_org_inn": [_("ИНН должен состоять из 9 цифр"), ]})
        return self.cleaned_data

    class Meta:
        fields = ("entity_payer_org_name", "entity_payer_address", "entity_payer_phone_number", "entity_payer_payment_account", "entity_payer_bank_name", "entity_payer_bank_code",
                  "entity_payer_bank_location", "entity_payer_org_inn", "entity_payer_registration_code", "entity_payer_org_class", "entity_payer_email", "entity_payer_head_name",)
        model = EntityPayer
        widgets = {'entity_payer_org_inn': forms.NumberInput(attrs={"class": "hide-arrows"})}


class SelfPaymentForm(forms.Form):
    self_payment = forms.BooleanField(label=_("Обучаюсь сам"), initial=False, required=False)


class ConfirmationForm(forms.ModelForm):
    product = forms.ChoiceField(label=_("Выбор продукта"), choices=lazy(get_product_choices, tuple))

    def clean_product(self):
        p_class, p_id = self.cleaned_data.get("product").split("-")
        if p_class == "course":
            obj = Course.objects.filter(id=p_id)
            self.cleaned_data["is_course"] = True
        elif p_class == "training":
            obj = Training.objects.filter(id=p_id)
            self.cleaned_data["is_course"] = False
        else:
            raise ValidationError({"product": [_("Продукт не найден"), ]})

        if obj.exists():
            self.cleaned_data["p_id"] = p_id
        else:
            raise ValidationError({"product": [_("Продукт не найден"), ]})

        return self.cleaned_data

    class Meta:
        model = PurchaseRecord
        fields = ("product", "language", "study_type", "special_price")

class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["payment_type"].required = True
        if kwargs.get("instance"):
            self.fields["payment_type"].choices = kwargs.get("instance").get_payment_type_choices()

    class Meta:
        model = PurchaseRecord
        fields = ("payment_type", )
