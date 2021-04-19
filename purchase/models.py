from pathlib import Path

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import validate_integer
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.safestring import mark_safe

from django.utils.translation import gettext_lazy as _, gettext as gt

from bbu_academy.settings import BASE_DIR
from payme_billing.mixins import PaymeMerchantMixin

EDUCATION = (
    ("secondary", _("Среднее")),
    ("secondary_special", _("Средне-специальное")),
    ("higher", _("Высшее образование"))
)

STUDY_TYPE_CHOICES = (
    ("intramural", _("Офлайн обучение")),
    ("remote", _("Дистанционное обучение"))
)

STUDY_TYPE_ABBREVIATIONS = {
    "intramural": "",
    "remote": "D"
}

PAYMENT_TYPE_CHOICES = (
    ("payme", "PayMe"),
    ("bank", _("Оплата через банк"))
)


STUDENT_PASSPORT_SLUG = "student_passport"
STUDY_DOCUMENT_SLUG = "study_document"
PAYER_PASSPORT_SLUG = "payer_passport"
INVOICE_SLUG = "invoice"

PURCHASE_DOCS_FOLDER = BASE_DIR / "media" / "temp" / "purchase_docs"
PURCHASE_DOCS_BASE_LINK = "/media/temp/purchase_docs/"


class Student(models.Model):
    student_full_name = models.CharField(_("ФИО студента"), help_text=_("(полностью, как в паспорте)"), max_length=300)
    student_inn = models.CharField(_("ИНН студента"), validators=[validate_integer], max_length=30)
    student_passport_n = models.CharField(_("Номер паспорта студента"), max_length=30)
    student_passport_received_date = models.DateField(_("Дата выдачи паспорта студента"))
    student_passport_given_by = models.CharField(_("Кем выдан паспорт студента"), max_length=300)
    student_phone_number = models.CharField(_("Номер телефона"), max_length=40)
    student_email = models.EmailField(_("Адрес электронной почты"))
    student_telegram_contact = models.CharField(_("Контакт в Telegram (если имеется)"), help_text=_("(номер телефона, ссылка или юзернейм)"), max_length=300, null=True, blank=True)
    study_type = models.CharField(_("Образование"), choices=EDUCATION, max_length=40)
    record = models.ForeignKey(verbose_name="Запись", to="PurchaseRecord", on_delete=models.CASCADE, related_name="students")

    def __str__(self):
        return self.name

    def __iter__(self):
        for field in self._meta.fields:
            yield field.verbose_name, field.value_to_string(self)

    def _name_of(self, filename):
        for item in self.folder_path.iterdir():
            if filename in item.name:
                return item.name

    @property
    def folder_path(self) -> Path:
        path = self.record.folder_path / f"student_{self.id}"
        path.mkdir(exist_ok=True, parents=True)
        return path

    @property
    def passport_path(self) -> Path:
        name = self._name_of(STUDENT_PASSPORT_SLUG)
        return self.folder_path / name if name else None

    @property
    def study_document_path(self) -> Path:
        name = self._name_of(STUDY_DOCUMENT_SLUG)
        return self.folder_path / name if name else None

    def passport_link(self) -> str:
        name = self._name_of(STUDENT_PASSPORT_SLUG)
        return PURCHASE_DOCS_BASE_LINK + f"record_{self.record.id}/student_{self.id}/" + name if name else ""

    def study_document_link(self) -> str:
        name = self._name_of(STUDY_DOCUMENT_SLUG)
        return PURCHASE_DOCS_BASE_LINK + f"record_{self.record.id}/student_{self.id}/" + name if name else ""

    def save_passport(self, file: InMemoryUploadedFile):
        if self.passport_path:
            self.passport_path.unlink()
        default_storage.save(self.folder_path / f"{STUDENT_PASSPORT_SLUG}{Path(file.name).suffix}".replace(" ", "_"), ContentFile(file.open().read()))

    def save_study_document(self, file: InMemoryUploadedFile):
        if self.study_document_path:
            self.study_document_path.unlink()
        default_storage.save(self.folder_path / f"{STUDY_DOCUMENT_SLUG}{Path(file.name).suffix}".replace(" ", "_"), ContentFile(file.open().read()))

    def delete_temp_files(self):
        if self.passport_path:
            self.passport_path.unlink()
        if self.study_document_path:
            self.study_document_path.unlink()
        self.folder_path.rmdir()

    @property
    def name(self):
        return self.student_full_name

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"


class IndividualPayer(models.Model):
    individual_payer_full_name = models.CharField(_("ФИО плательщика"), help_text=_("(полностью, как в паспорте)"), max_length=300)
    individual_payer_inn = models.CharField(_("ИНН плательщика"), validators=[validate_integer], max_length=30)
    individual_payer_passport_n = models.CharField(_("Номер паспорта плательщика"), max_length=30)
    individual_payer_passport_received_date = models.DateField(_("Дата выдачи паспорта плательщика"))
    individual_payer_passport_given_by = models.CharField(_("Кем выдан паспорт плательщика"), max_length=300)
    individual_payer_phone_number = models.CharField(_("Номер телефона"), max_length=40)
    individual_payer_email = models.EmailField(_("Адрес электронной почты"))
    individual_payer_telegram_contact = models.CharField(_("Контакт в Telegram (если имеется)"), help_text=_("(номер телефона или ссылка)"), max_length=300, null=True, blank=True)
    record = models.OneToOneField(verbose_name="Запись", to="PurchaseRecord", on_delete=models.CASCADE, related_name="individual_payer")

    def __str__(self):
        return self.name

    def __iter__(self):
        for field in self._meta.fields:
            yield field.verbose_name, field.value_to_string(self)

    def email(self):
        return self.individual_payer_email

    @property
    def phone(self):
        return self.individual_payer_phone_number

    @property
    def name(self):
        return self.individual_payer_full_name

    @property
    def inn(self):
        return self.individual_payer_inn

    @property
    def folder_path(self) -> Path:
        path = self.record.folder_path / f"payer"
        path.mkdir(exist_ok=True, parents=True)
        return path

    @property
    def passport_path(self) -> Path:
        for item in self.folder_path.iterdir():
            if PAYER_PASSPORT_SLUG in item.name:
                return self.folder_path / item.name

    def save_passport(self, file: InMemoryUploadedFile):
        if self.passport_path:
            self.passport_path.unlink()
        default_storage.save(self.folder_path / f"{PAYER_PASSPORT_SLUG}{Path(file.name).suffix}", ContentFile(file.open().read()))

    def delete_temp_files(self):
        if self.passport_path:
            self.passport_path.unlink()
        self.folder_path.rmdir()

    class Meta:
        verbose_name = "Физическое лицо"
        verbose_name_plural = "Физические лица"


class EntityPayer(models.Model):
    entity_payer_org_name = models.CharField(_("Наименование организации"), max_length=300)
    entity_payer_address = models.CharField(_("Адрес"), max_length=500)
    entity_payer_phone_number = models.CharField(_("Номер телефона"), max_length=40)
    entity_payer_payment_account = models.CharField(_("Расчётный счёт"), max_length=100)
    entity_payer_bank_name = models.CharField(_("Наименование банка"), max_length=300)
    entity_payer_bank_code = models.CharField(_("Код банка"), max_length=100)
    entity_payer_bank_location = models.CharField(_("Город местанахождения банка"), max_length=200)
    entity_payer_org_inn = models.CharField(_("ИНН организации"), validators=[validate_integer], max_length=30)
    entity_payer_registration_code = models.CharField(_("Регистрационный код плательщика НДС"), max_length=100, null=True, blank=True)
    entity_payer_org_class = models.CharField(_("ОКЭД организации"), max_length=100)
    entity_payer_email = models.EmailField(_("Адрес электронной почты"))
    entity_payer_head_name = models.CharField(_("ФИО и должность руководителя"), max_length=300)
    record = models.OneToOneField(verbose_name="Запись", to="PurchaseRecord", on_delete=models.CASCADE, related_name="entity_payer")

    def __str__(self):
        return self.name

    def __iter__(self):
        for field in self._meta.fields:
            yield field.verbose_name, field.value_to_string(self)

    def email(self):
        return self.entity_payer_email

    @property
    def phone(self):
        return self.entity_payer_phone_number

    @property
    def name(self):
        return self.entity_payer_org_name

    @property
    def inn(self):
        return self.entity_payer_org_inn

    def delete_temp_files(self):
        pass

    class Meta:
        verbose_name = "Юридическое лицо"
        verbose_name_plural = "Юридические лица"


class PurchaseRecord(PaymeMerchantMixin):
    offer_agreement = models.BooleanField("Пользовательское соглашение", default=False)
    date_started = models.DateTimeField("Дата и время создания заказа", auto_now_add=True)
    date_finished = models.DateTimeField("Дата и время завершения заказа", null=True, blank=True)
    study_type = models.CharField(verbose_name=_("Тип обучения"), choices=STUDY_TYPE_CHOICES, max_length=20)

    content_type = models.ForeignKey(verbose_name="Продукт", to=ContentType, related_name="content_type_timelines", on_delete=models.DO_NOTHING, null=True, blank=True,
                                     limit_choices_to=models.Q(app_label='trainings', model='training', active=True) | models.Q(app_label='courses', model='course'))
    object_id = models.PositiveIntegerField(null=True, blank=True)
    product = GenericForeignKey()

    special_price = models.BooleanField(_("Я являюсь членом АТБ"), default=False)
    price = models.BigIntegerField("Цена на курс/тренинг", null=True, blank=True)
    overall_price = models.BigIntegerField("Общая цена", null=True, blank=True)
    payment_type = models.CharField(_("Тип оплаты"), max_length=30, choices=PAYMENT_TYPE_CHOICES, null=True, blank=True)
    finished = models.BooleanField("Завершено", default=False)
    is_paid = models.BooleanField("Оплачено", default=False, help_text="В случае с оплатой через банк, галочка должна быть поставлена вручную")

    def __str__(self):
        return f"Покупка - {self.payer_name()}"

    def get_amount(self):
        return self.overall_price

    def get_payment_type_choices(self):
        if self.get_entity_payer_or_none():
            return (PAYMENT_TYPE_CHOICES[1],)
        else:
            return PAYMENT_TYPE_CHOICES

    def complete_payment(self):
        self.is_paid = True
        self.finished = True
        self.save()
        self.delete_temp_files()

    def finish(self):
        self.finished = True
        self.save()
        self.delete_temp_files()

    def get_9_digit_phone(self):
        return ''.join(filter(lambda x: x.isdigit(), self.phone))[-9:]

    def f_price(self):
        line = str(self.price)[::-1]
        return " ".join([line[i:i+3] for i in range(0, len(line), 3)])[::-1] + " " + gt("сум")

    def f_overall_price(self):
        line = str(self.overall_price)[::-1]
        return " ".join([line[i:i+3] for i in range(0, len(line), 3)])[::-1] + " " + gt("сум")

    def payer_type(self):
        return self.payer._meta.verbose_name if self.payer else "(не заполнено)"
    payer_type.short_description = "Тип плательщика"

    def student_name(self):
        students = self.students
        return students.first().name if students.count() == 1 else f"Студенты ({students.count()})"
    student_name.short_description = "Студент(ы)"

    def payer_name(self):
        return self.payer.name if self.payer else "(не заполнено)"
    payer_name.short_description = "Плательщик"

    @property
    def payer(self):
        try:
            return self.individual_payer
        except ObjectDoesNotExist:
            try:
                return self.entity_payer
            except ObjectDoesNotExist:
                return None

    @property
    def phone(self):
        if not self.payer:
            return None
        else:
            return self.payer.phone

    def get_individual_payer_or_none(self):
        try:
            return self.individual_payer
        except ObjectDoesNotExist:
            return None

    def get_entity_payer_or_none(self):
        try:
            return self.entity_payer
        except ObjectDoesNotExist:
            return None

    @property
    def folder_path(self) -> Path:
        path = PURCHASE_DOCS_FOLDER / f"record_{self.id}"
        path.mkdir(exist_ok=True, parents=True)
        return path

    @property
    def invoice_path(self) -> Path:
        return self.folder_path / f"{INVOICE_SLUG}.pdf"

    def admin_invoice_link(self):
        if self.invoice_path.exists():
            return mark_safe(f"""<b><a target="_blank" href="{self.invoice_link}">Посмотреть счёт</a></b>""")
        else:
            return mark_safe("<b>Ещё не создан</b>")
    admin_invoice_link.short_description = "Счёт"

    @property
    def invoice_link(self) -> str:
        return PURCHASE_DOCS_BASE_LINK + f"record_{self.id}/{INVOICE_SLUG}.pdf" if self.invoice_path.exists() else ""

    def delete_temp_files(self):
        try:
            for student in self.students.all():
                student.delete_temp_files()
            if self.payer:
                self.payer.delete_temp_files()
        except Exception as e:
            print(e)

    def entity_form_is_ready(self):
        return self.students.exists() and self.get_entity_payer_or_none()

    def individual_form_is_ready(self):
        return self.students.exists() and self.get_individual_payer_or_none()

    def is_ready(self):
        return self.entity_form_is_ready() or self.individual_form_is_ready()

    def is_confirmed(self):
        return self.object_id is not None and self.special_price is not None and self.price is not None and self.overall_price is not None

    def study_type_abbreviation(self):
        return STUDY_TYPE_ABBREVIATIONS.get(self.study_type)

    def dotted_date_finished(self):
        return self.date_finished.strftime("%d.%m.%Y")

    def invoice_payer_name(self):
        return self.payer.name

    def invoice_address(self):
        return self.get_entity_payer_or_none().entity_payer_address if self.get_entity_payer_or_none() else None

    def invoice_inn(self):
        return self.payer.inn

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
