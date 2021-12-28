from django import forms
from django.core.validators import FileExtensionValidator
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from certificates.models import Certificate
from certificates.utils import parse_excel, populate_certificate, broken_certificates_report

ACTION_CHOICES = (
    ("skip", "Пропустить существующие сертификаты"),
    ("renew", "Обновить существующие сертификаты"),
)


class RegistryForm(forms.Form):
    pinfl_or_inn = forms.IntegerField(widget=forms.TextInput(attrs={"class": "w-100 mt-20 fname", "placeholder": _("Введите ПИНФЛ или ИНН")}))


class CertificateAdminForm(forms.ModelForm):
    def clean(self):
        certificate_n = self.cleaned_data.get("certificate_n", None)
        if certificate_n:
            certificate_n = str(int(certificate_n))
            certificate_n = "0" * (3-len(certificate_n)) + certificate_n
            self.cleaned_data["certificate_n"] = certificate_n

    class Meta:
        widgets = {
            "inn": forms.NumberInput(attrs={"step": "1"}),
            "pinfl": forms.NumberInput(attrs={"step": "1"}),
            "certificate_n": forms.NumberInput(attrs={"step": "1"}),
            "contract_n": forms.NumberInput(attrs={"step": "1"}),
        }


class MultiCertificateAdminForm(forms.ModelForm):
    certificates = forms.FileField(
        widget=forms.FileInput(),
        validators=[FileExtensionValidator(allowed_extensions=['xls', 'xlt', 'xlm', 'xlsx', 'xlsm', 'xltx', 'xltm', 'xlsb', 'xla', 'xlam', 'xll', 'xlw'],
                                           message="Пожалуста, загрузите Excel файл"), ],
        label="Загрузите файл Excel с сертификатами",
    )
    existing_action = forms.ChoiceField(
        widget=widgets.RadioSelect(),
        choices=ACTION_CHOICES,
        initial="skip",
        label="Существующие сертификаты",
        help_text="Выберите действие для существующих сертификатов",
    )

    def save_certificates(self):
        cleaned_certificates = self.cleaned_data.get('certificates')
        cleaned_choice = self.cleaned_data.get('existing_action')

        correct_certificates, broken_certificates = parse_excel(cleaned_certificates)

        created_n = 0
        renewed_n = 0
        skipped_n = 0

        for parsed_certificate in correct_certificates:
            if parsed_certificate.inn is not None:
                model_certificate = Certificate(inn=parsed_certificate.inn)
                created = not Certificate.objects.filter(inn=parsed_certificate.inn).exists()
            else:
                model_certificate = Certificate(pinfl=parsed_certificate.pinfl)
                created = not Certificate.objects.filter(pinfl=parsed_certificate.pinfl).exists()

            if created or cleaned_choice == "renew":
                populate_certificate(model_certificate, parsed_certificate)
                model_certificate.save()
                created_n += 1
            else:
                skipped_n += 1

        incorrect_certificates_n, report = broken_certificates_report(broken_certificates)

        return created_n, renewed_n, skipped_n, incorrect_certificates_n, report

    def as_django_admin(self):
        from formadmin.forms import as_django_admin
        return as_django_admin(self)

    class Meta:
        fields = ("certificates", "existing_action")
        model = Certificate
