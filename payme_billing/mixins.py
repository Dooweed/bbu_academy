from abc import abstractmethod

from django.db import models

from payme_billing.vars.static import PAYME_RECEIPT_STATES


class PaymeMerchantMixin(models.Model):
    state = models.IntegerField("Состояние чека (PayMe)", choices=PAYME_RECEIPT_STATES, default=0)
    is_paid = models.BooleanField("Оплачено", default=False, help_text="В случае с оплатой через банк, галочка должна быть поставлена вручную")

    @abstractmethod
    def get_amount(self) -> int:  # Should be overridden to return integer, representing amount (full cost) for order
        pass

    @abstractmethod
    def complete_payment(self):  # Should be overridden to finish payment
        pass

    class Meta:
        abstract = True
