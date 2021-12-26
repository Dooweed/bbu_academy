from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from image_cropping import ImageRatioField

from tools.description_mixin import DescriptionMixin
from tools.image_mixin import ImageMixin


class Service(ImageMixin, DescriptionMixin):
    SHORT_TITLE_LENGTH = 60

    title = models.CharField("Название услуги", max_length=500)
    url = AutoSlugField(verbose_name="URL услуги", unique=True, populate_from='title', editable=True)
    active = models.BooleanField("Активно", help_text="Неактивные услуги не будут отображаться на сайте", default=True)

    image = models.ImageField("Изображение", upload_to="trainings/", help_text="Возможность обрезки появится после сохранения", null=True, blank=True)
    thumbnail_size = ImageRatioField(verbose_name="Обрезка изображения для превью (список услуг)", image_field='image', size="512x288")
    sidebar_size = ImageRatioField(verbose_name="Обрезка изображения для превью (сайдбар)", image_field='image', size="140x140")

    price = models.IntegerField("Цена на услугу")
    special_price = models.IntegerField("Специальная цена на услугу")

    sorting = models.PositiveIntegerField("Порядок отображения в списках", default=0, blank=False, null=False)

    def __str__(self):
        return self.title

    def beautified_price(self):
        price = str(self.price)[::-1]
        price = " ".join([price[i:i+3] for i in range(0, len(price), 3)])[::-1]
        return price + " " + _("сум")

    def short_title(self):
        if len(self.title) > self.SHORT_TITLE_LENGTH:
            cut = self.title[:self.SHORT_TITLE_LENGTH-3]
            return cut[:cut.rfind(' ')] + "..."
        else:
            return self.title

    def get_absolute_url(self):
        return reverse('services:service', args=(self.url,))

    class Meta:
        ordering = ['sorting']
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
