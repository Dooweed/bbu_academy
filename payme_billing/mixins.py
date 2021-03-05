from abc import abstractmethod

from django.db import models

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

class PaymeStateMixin(models.Model):
    state = models.IntegerField("Состояние чека (PayMe)", choices=PAYME_RECEIPT_STATES, default=0)

    @abstractmethod
    def get_amount(self) -> int:  # Should be overridden to return integer, representing amount (full cost) for order
        pass

    class Meta:
        abstract = True
