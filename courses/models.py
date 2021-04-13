from autoslug import AutoSlugField
from django.db import models

from image_cropping import ImageRatioField
from django.utils.translation import gettext as _

from tools.description_mixin import DescriptionMixin
from tools.image_mixin import ImageMixin


class Course(ImageMixin, DescriptionMixin):
    SHORT_TITLE_LENGTH = 60

    title = models.CharField("Название курса", max_length=500)
    url = AutoSlugField(verbose_name="URL курса", unique=True, populate_from='title', editable=True)
    active = models.BooleanField("Активно", help_text="Неактивные курсы не будут отображаться на сайте", default=True)

    image = models.ImageField("Изображение", upload_to="courses/", help_text="Возможность обрезки появится после сохранения", null=True, blank=True)
    sidebar_size = ImageRatioField(verbose_name="Обрезка изображения для превью (сайдбар)", image_field='image', size="140x140")
    thumbnail_size = ImageRatioField(verbose_name="Обрезка изображения для превью (список курсов)", image_field='image', size="512x288")

    offline_price = models.IntegerField("Цена на курс (Офлайн)")
    offline_special_price = models.IntegerField("Специальная цена на курс (Офлайн)")
    online_price = models.IntegerField("Цена на курс (Онлайн)")
    online_special_price = models.IntegerField("Специальная цена на курс (Онлайн)")

    sorting = models.PositiveIntegerField("Порядок отображения в списках", default=0, blank=False, null=False)

    def __str__(self):
        return self.title

    def online_beautified_price(self):
        price = str(self.online_price)[::-1]
        price = " ".join([price[i:i+3] for i in range(0, len(price), 3)])[::-1]
        return price + " " + _("сум")

    def offline_beautified_price(self):
        price = str(self.offline_price)[::-1]
        price = " ".join([price[i:i+3] for i in range(0, len(price), 3)])[::-1]
        return price + " " + _("сум")

    def short_title(self):
        if len(self.title) > self.SHORT_TITLE_LENGTH:
            cut = self.title[:self.SHORT_TITLE_LENGTH-3]
            return cut[:cut.rfind(' ')] + "..."
        else:
            return self.title

    class Meta:
        ordering = ['sorting']
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
