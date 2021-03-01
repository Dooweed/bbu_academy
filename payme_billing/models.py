from django.db import models

from django.utils import timezone


TRANSACTION_TIMEOUT = 43200  # In seconds, equal to 12 hours

PAYME_TRANSACTION_STATES = (
    (1, "Транзакция успешно создана, ожидание подтверждения (начальное состояние 0)"),
    (2, "Транзакция успешно завершена (начальное состояние 1)"),
    (-1, "Транзакция отменена (начальное состояние 1)"),
    (-2, "Транзакция отменена после завершения (начальное состояние 2)"),
)

PAYME_TRANSACTION_DENIAL_REASONS = (
    (1, "Один или несколько получателей не найдены или неактивны в Payme Business."),
    (2, "Ошибка при выполнении дебетовой операции в процессинговом центре."),
    (3, "Ошибка выполнения транзакции."),
    (4, "Транзакция отменена по таймауту."),
    (5, "Возврат денег."),
    (10, "Неизвестная ошибка."),
)

PAYME_RECEIPT_STATES = (
    (0, "Чек создан. Ожидание подтверждения оплаты."),
    (1, "Первая стадия проверок. Создание транзакции в биллинге мерчанта."),
    (2, "Списание денег с карты."),
    (3, "Закрытие транзакции в биллинге мерчанта."),
    (4, "Чек оплачен."),
    (20, "Чек стоит на паузе для ручного вмешательства."),
    (21, "Чек в очереди на отмену."),
    (30, "Чек в очереди на закрытие транзакции в биллинге мерчанта."),
    (50, "Чек отменен."),
)


class PaymeTransaction(models.Model):
    record_id = models.IntegerField("Номер записи")
    transaction_id = models.CharField("Идентификатор транзакции", max_length=24, unique=True, primary_key=True)
    amount = models.PositiveBigIntegerField("Цена")
    creation_time = models.DateTimeField("Дата и время создания транзакции", auto_now_add=True)
    perform_time = models.DateTimeField("Дата и время осуществления транзакции", null=True, blank=True)
    state = models.IntegerField("Состояние транзакции", choices=PAYME_TRANSACTION_STATES, default=0)
    denial_reason = models.CharField("Причина отмены транзакции", choices=PAYME_TRANSACTION_DENIAL_REASONS, max_length=200, null=True, blank=True)
    phone = models.CharField("Номер телефона плательщика", max_length=200)

    def __str__(self):
        return f"Транзакция по номеру {self.phone}, id={self.transaction_id}"

    def is_timed_out(self):
        return (timezone.now() - self.creation_time).seconds >= TRANSACTION_TIMEOUT

    class Meta:
        verbose_name = "Payme транзакция"
        verbose_name_plural = "Payme транзакции"
