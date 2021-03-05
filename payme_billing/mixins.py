from abc import abstractmethod

from django.db import models

class PaymeStateMixin(models.Model):
    state = models.IntegerField("Состояние чека (PayMe)", choices=PAYME_RECEIPT_STATES, default=0)

    @abstractmethod
    def get_amount(self) -> int:  # Should be overridden to return integer, representing amount (full cost) for order
        pass

    class Meta:
        abstract = True
