from django.db import models

from django.utils import timezone

from payme_billing.vars.static import PAYME_TRANSACTION_STATES, PAYME_TRANSACTION_DENIAL_REASONS

TRANSACTION_TIMEOUT = 43200  # In seconds, equal to 12 hours


class PaymeTransaction(models.Model):
    record_id = models.IntegerField("Номер записи", unique=True)
    transaction_id = models.CharField("Идентификатор транзакции", max_length=24, unique=True, primary_key=True)
    amount = models.PositiveBigIntegerField("Цена")
    state = models.IntegerField("Состояние транзакции", choices=PAYME_TRANSACTION_STATES, default=0)
    denial_reason = models.IntegerField("Причина отмены транзакции", choices=PAYME_TRANSACTION_DENIAL_REASONS, null=True, blank=True)
    phone = models.CharField("Номер телефона плательщика", max_length=200, blank=True)

    creation_time = models.DateTimeField("Дата и время создания транзакции", auto_now_add=True)
    perform_time = models.DateTimeField("Дата и время осуществления транзакции", null=True, blank=True)
    cancel_time = models.DateTimeField("Дата и время отмены транзакции", null=True, blank=True)
    payme_creation_time = models.DateTimeField("Дата и время создания транзакции на сервере Payme")

    def __str__(self):
        return f"Транзакция по номеру {self.phone}, id={self.transaction_id}"

    def is_timed_out(self):
        return (timezone.now() - self.creation_time).seconds >= TRANSACTION_TIMEOUT

    def get_creation_time(self):
        return int(self.creation_time.timestamp()*1000) if self.creation_time else 0

    def get_perform_time(self):
        return int(self.perform_time.timestamp()*1000) if self.perform_time else 0

    def get_cancel_time(self):
        return int(self.cancel_time.timestamp()*1000) if self.cancel_time else 0

    def get_payme_creation_time(self):
        return int(self.payme_creation_time.timestamp()*1000) if self.payme_creation_time else 0

    class Meta:
        verbose_name = "Payme транзакция"
        verbose_name_plural = "Payme транзакции"
