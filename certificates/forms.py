from django import forms
from django.core.validators import FileExtensionValidator
from django.forms import widgets

from certificates.models import Certificate
from certificates.utils import parse_excel, populate_certificate, broken_certificates_report

ACTION_CHOICES = (
    ("skip", "Пропустить существующие сертификаты"),
    ("renew", "Обновить существующие сертификаты"),
)


class RegistryForm(forms.Form):
    inn = forms.IntegerField(widget=forms.TextInput(attrs={"class": "w-100 mt-20 fname", "placeholder": "Введите ИНН"}))


class CertificateAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            "inn": forms.NumberInput(),
            "certificate_n": forms.NumberInput(),
            "contract_n": forms.NumberInput(),
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
            model_certificate = Certificate.objects.filter(inn=parsed_certificate.inn)
            if model_certificate.exists():
                model_certificate = model_certificate.first()
                created = False
            else:
                model_certificate = Certificate(inn=parsed_certificate.inn)
                created = True
            if created:
                populate_certificate(model_certificate, parsed_certificate)
                model_certificate.save()
                created_n += 1
            elif cleaned_choice == "renew":
                populate_certificate(model_certificate, parsed_certificate)
                model_certificate.save()
                renewed_n += 1
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

# class PhotoGalleryAdminForm(forms.ModelForm):
#
#     class Media:
#         js = ('js/select_all_button.js', )
#
#     images = forms.FileField(
#         widget=forms.ClearableFileInput(attrs={"multiple": True}),
#         label="Добавить сразу несколько изображений",
#         required=False,
#     )
#     size_restriction = forms.IntegerField(
#         label="Ограничение по размеру",
#         help_text="Ограничение по размеру применяется к наибольшей стороне изображения. Оставьте поле пустым чтобы оставить изображения в исходном размере",
#         min_value=0,
#         required=False)
#
#     def clean_photos(self):
#         """Make sure only images can be uploaded."""
#         for upload in self.files.getlist("images"):
#             validate_image_file_extension(upload)
#
#     def save_photos(self, gallery):
#         """Process each uploaded image."""
#         if 'size_restriction' in self.cleaned_data:
#             size_restriction = self.cleaned_data['size_restriction']
#         else:
#             size_restriction = None
#         for upload in self.files.getlist("images"):
#             upload.name = translit(upload.name, 'ru', reversed=True)
#             if size_restriction:
#                 image = Image.open(upload)
#                 w, h = image.size
#                 if w > size_restriction or h > size_restriction:
#                     if w > h:
#                         image = image.resize((size_restriction, int(size_restriction*(h/w))), Image.ANTIALIAS)
#                     else:
#                         image = image.resize((int(size_restriction*(w/h)), size_restriction), Image.ANTIALIAS)
#                     output = io.BytesIO()
#                     image.save(output, format=upload.content_type.split("/")[-1])
#                     output.seek(0)
#                     upload = InMemoryUploadedFile(output, None, upload.name, upload.content_type,
#                                                   output.tell(), upload.charset, upload.content_type_extra)
#             image_obj = Photo(gallery=gallery, image=upload)
#             image_obj.save()
