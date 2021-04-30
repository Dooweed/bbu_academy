from django.apps import AppConfig


class PurchaseConfig(AppConfig):
    name = 'purchase'
    verbose_name = "Покупки"

    def ready(self):
        from purchase.models import PurchaseRecord, Student, IndividualPayer
        from django.db.models.signals import pre_delete
        from purchase.signals.signals import temp_files_delete

        pre_delete.connect(temp_files_delete, sender=PurchaseRecord)
        pre_delete.connect(temp_files_delete, sender=Student)
        pre_delete.connect(temp_files_delete, sender=IndividualPayer)
