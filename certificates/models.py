from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, validate_integer


# Create your models here.

class Certificate(models.Model):
    contract_n = models.IntegerField("Номер договора", null=True, blank=True)
    certificate_n = models.CharField("Номер сертификата", max_length=20, validators=[validate_integer, ])
    inn = models.PositiveBigIntegerField("ИНН студента", validators=[MinValueValidator, MaxValueValidator], unique=True)
    full_name = models.CharField("ФИО студента", max_length=200)
    date_received = models.DateField("Дата получения договора")

    def get_day(self):
        return f"{self.date_received.day:02}"

    def get_month(self):
        return f"{self.date_received.month:02}"

    def get_year(self):
        return f"{self.date_received.year:02}"

    def get_short_year(self):
        return str(self.date_received.year)[-2:]

    def dotted_date(self):
        return self.date_received.strftime("%d.%m.%Y")

    def __str__(self):
        return f"Сертификат #{self.certificate_n}, {self.full_name}"

    class Meta:
        ordering = ["date_received"]
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"
