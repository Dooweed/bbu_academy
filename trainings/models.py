from autoslug import AutoSlugField
from django.db import models
from django.utils.safestring import mark_safe
from django.utils import timezone

from image_cropping import ImageRatioField

from tools.description_mixin import DescriptionMixin
from tools.image_mixin import ImageMixin


class Training(ImageMixin, DescriptionMixin):
    SHORT_TITLE_LENGTH = 60

    title = models.CharField("Название тренинга", max_length=500)
    url = AutoSlugField(verbose_name="URL тренинга", unique=True, populate_from='title', editable=True)
    active = models.BooleanField("Активно", help_text="Неактивные тренинги не будут отображаться на сайте", default=True)

    image = models.ImageField("Изображение", help_text="Возможность обрезки появится после сохранения", null=True, blank=True)
    thumbnail_size = ImageRatioField(verbose_name="Обрезка изображения для превью (список тренингов)", image_field='image', size="512x288")
    sidebar_size = ImageRatioField(verbose_name="Обрезка изображения для превью (сайдбар)", image_field='image', size="140x140")

    price = models.IntegerField("Цена на курс")
    # location = models.CharField("Место проведения тренинга", max_length=500)
    # date_arranged = models.DateTimeField("Дата и время проведения тренинга", help_text="При отсутсвии даты будет отображено \"Скоро\"", blank=True, null=True)
    sorting = models.PositiveIntegerField("Порядок отображения в списках", default=0, blank=False, null=False)

    def __str__(self):
        return self.title

    def f_price(self):
        line = str(self.price)[::-1]
        return " ".join([line[i:i+3] for i in range(0, len(line), 3)])[::-1]

    def short_title(self):
        if len(self.title) > self.SHORT_TITLE_LENGTH:
            cut = self.title[:self.SHORT_TITLE_LENGTH-3]
            return cut[:cut.rfind(' ')] + "..."
        else:
            return self.title

    # def passed(self):
    #     return timezone.now() >= self.date_arranged
    #
    # def date_string(self):
    #     return mark_safe(f"""<b><i>{self.date_arranged.strftime("%d.%m.%Y, %H:%M") if self.date_arranged else "Скоро"}</i></b>""")

    class Meta:
        ordering = ['sorting']
        verbose_name = "Тренинг"
        verbose_name_plural = "Тренинги"
