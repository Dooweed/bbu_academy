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

from bbu_academy.settings import MEDIA_ROOT
from payme_billing.mixins import PaymeMerchantMixin
from tools.utils import link_tag, pinfl_help_text

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

LANGUAGE_CHOICES = (
    ("ru", _("Русский")),
    ("uz", _("Узбекский"))
)


PASSPORT_SLUG = "passport"
INVOICE_SLUG = "invoice"

PURCHASE_DOCS_FOLDER = Path(MEDIA_ROOT) / "temp" / "s_purchase_docs"
PURCHASE_DOCS_BASE_LINK = "/media/temp/s_purchase_docs/"


class IndividualPayer(models.Model):
    full_name = models.CharField(_("ФИО"), help_text=mark_safe(f'<span class="text-danger font-weight-bold">{_("(полностью, как в паспорте, латиницей)")}</span>'),
                                 max_length=300)
    pinfl = models.CharField(_("ПИНФЛ"), validators=[validate_integer], help_text=mark_safe(pinfl_help_text), max_length=30)
    passport_n = models.CharField(_("Номер паспорта"), max_length=30)
    phone_number = models.CharField(_("Номер телефона"), max_length=40)
    email = models.EmailField(_("Адрес электронной почты"))
    telegram_contact = models.CharField(_("Контакт в Telegram (если имеется)"), help_text=_("(номер телефона или ссылка)"), max_length=300, null=True, blank=True)
    record = models.OneToOneField(verbose_name="Запись", to="SmallPurchaseRecord", on_delete=models.CASCADE, related_name="individual_payer")

    def __str__(self):
        return self.name

    def __iter__(self):
        for field in self._meta.fields:
            yield field.verbose_name, field.value_to_string(self)

    @property
    def name(self):
        return self.full_name

    @property
    def folder_path(self) -> Path:
        path = self.record.folder_path
        path.mkdir(exist_ok=True, parents=True)
        return path

    @property
    def passport_path(self) -> Path:
        for item in self.folder_path.iterdir():
            if PASSPORT_SLUG in item.name:
                return self.folder_path / item.name

    def save_passport(self, file: InMemoryUploadedFile):
        if self.passport_path:
            self.passport_path.unlink()
        default_storage.save(self.folder_path / f"{PASSPORT_SLUG}{Path(file.name).suffix}", ContentFile(file.open().read()))

    def delete_temp_files(self):
        if self.passport_path:
            self.passport_path.unlink()
        self.folder_path.rmdir()

    class Meta:
        verbose_name = "Физическое лицо"
        verbose_name_plural = "Физические лица"


class EntityPayer(models.Model):
    org_name = models.CharField(_("Наименование организации"), max_length=300)
    address = models.CharField(_("Адрес"), max_length=500)
    phone_number = models.CharField(_("Номер телефона"), max_length=40)
    org_inn = models.CharField(_("ИНН организации"), validators=[validate_integer], max_length=30)
    email = models.EmailField(_("Адрес электронной почты"))
    head_name = models.CharField(_("ФИО и должность руководителя"), max_length=300)
    record = models.OneToOneField(verbose_name="Запись", to="SmallPurchaseRecord", on_delete=models.CASCADE, related_name="entity_payer")

    def __str__(self):
        return self.name

    def __iter__(self):
        for field in self._meta.fields:
            yield field.verbose_name, field.value_to_string(self)

    @property
    def name(self):
        return self.org_name

    @property
    def inn(self):
        return self.org_inn

    def delete_temp_files(self):
        pass

    class Meta:
        verbose_name = "Юридическое лицо"
        verbose_name_plural = "Юридические лица"


class SmallPurchaseRecord(PaymeMerchantMixin):
    offer_agreement = models.BooleanField("Пользовательское соглашение", default=False)
    date_started = models.DateTimeField("Дата и время создания заказа", auto_now_add=True)
    date_finished = models.DateTimeField("Дата и время завершения заказа", null=True, blank=True)
    service = models.ForeignKey(verbose_name=_('Услуга'), to='services.Service', on_delete=models.RESTRICT, null=True, blank=True)
    special_price = models.BooleanField(_("Я являюсь членом АТБ"), default=False)
    price = models.BigIntegerField("Цена на услугу", null=True, blank=True)
    amount = models.IntegerField(_('Кол-во наименований товаров'), null=True, blank=True)
    overall_price = models.BigIntegerField("Общая цена", null=True, blank=True)
    payment_type = models.CharField(_("Тип оплаты"), max_length=30, choices=PAYMENT_TYPE_CHOICES, null=True, blank=True)
    finished = models.BooleanField("Завершено", default=False)

    def __str__(self):
        return f'Покупка - {self.payer.name if self.payer else "(не заполнено)"}'

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

    def payer_type(self):
        return self.payer._meta.verbose_name if self.payer else "(не заполнено)"
    payer_type.short_description = "Тип плательщика"

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

    def invoice_n(self):
        return f"S{self.id}"
    invoice_n.short_description = "Номер счёта"

    def f_price(self):
        line = str(self.price)[::-1]
        return " ".join([line[i:i+3] for i in range(0, len(line), 3)])[::-1] + " " + gt("сум")

    def f_overall_price(self):
        line = str(self.overall_price)[::-1]
        return " ".join([line[i:i+3] for i in range(0, len(line), 3)])[::-1] + " " + gt("сум")

    @property
    def phone(self):
        if not self.payer:
            return None
        else:
            return self.payer.phone_number

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
        path = PURCHASE_DOCS_FOLDER / f"record_S{self.id}"
        path.mkdir(exist_ok=True, parents=True)
        return path

    @property
    def invoice_path(self) -> Path:
        return self.folder_path / f"{INVOICE_SLUG}.pdf"

    def admin_invoice_link(self):
        if self.invoice_path.exists():
            return mark_safe(f"""<b><a target="_blank" href="{self.invoice_link()}">Посмотреть счёт</a></b>""")
        else:
            return mark_safe("<b>Ещё не создан</b>")
    admin_invoice_link.short_description = "Счёт"

    def invoice_link(self) -> str:
        return PURCHASE_DOCS_BASE_LINK + f"record_S{self.id}/{INVOICE_SLUG}.pdf" if self.invoice_path.exists() else ""

    def delete_temp_files(self):
        try:
            if self.payer:
                self.payer.delete_temp_files()
        except Exception as e:
            print(e)

    def entity_form_is_ready(self):
        return self.get_entity_payer_or_none()

    def individual_form_is_ready(self):
        return self.get_individual_payer_or_none()

    def is_ready(self):
        return self.entity_form_is_ready() or self.individual_form_is_ready()

    def is_confirmed(self):
        return self.service is not None and self.special_price is not None and self.price is not None and self.overall_price is not None

    def dotted_date_finished(self):
        return self.date_finished.strftime("%d.%m.%Y")

    def invoice_payer_name(self):
        return self.payer.name

    def invoice_address(self):
        return self.get_entity_payer_or_none().address if self.get_entity_payer_or_none() else None

    def invoice_inn_or_pinfl(self):
        return self.payer.inn if self.get_individual_payer_or_none() is None else self.payer.pinfl

    class Meta:
        verbose_name = "Мини-покупка"
        verbose_name_plural = "Мини-покупки"
