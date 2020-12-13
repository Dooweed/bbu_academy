from django.db import models

from image_cropping import ImageRatioField

from tools.date_mixin import DateMixin
from tools.description_mixin import DescriptionMixin
from tools.image_mixin import ImageMixin
from tools.utils import delete_unused_thumbnails
from autoslug import AutoSlugField
from django_cleanup.signals import cleanup_post_delete

# Signals
cleanup_post_delete.connect(delete_unused_thumbnails)


# Models

class ArticleCategory(models.Model):
    name = models.CharField("Название категории", max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория статей"
        verbose_name_plural = "Категории статей"


class Article(ImageMixin, DateMixin, DescriptionMixin):
    SHORT_TITLE_LENGTH = 60
    CONDITIONS = (("editing", "Редактирование"), ("pending", "Ожидание"), ("published", "Опубликовано"),)

    title = models.CharField("Заголовок статьи", max_length=500)
    url = AutoSlugField(verbose_name="URL статьи", unique=True, populate_from='title', editable=True)
    status = models.CharField("Состояние статьи", help_text="Отображаться будут только статьи с состоянием \"Опубликовано\"", default="editing", max_length=30, choices=CONDITIONS)
    image = models.ImageField("Изображение статьи", help_text="Возможность обрезки появится после сохранения", upload_to="articles/", null=True, blank=True)
    category = models.ForeignKey(verbose_name="Категории", to=ArticleCategory, on_delete=models.DO_NOTHING, null=True, blank=True)

    thumbnail_size = ImageRatioField(verbose_name="Обрезка изображения для превью", image_field='image', size="512x288")

    def __str__(self):
        return self.title

    def active(self):
        return self.status == "published"

    def short_title(self):
        if len(self.title) > self.SHORT_TITLE_LENGTH:
            cut = self.title[:self.SHORT_TITLE_LENGTH-3]
            return cut[:cut.rfind(' ')] + "..."
        else:
            return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

        ordering = ['-date']


Article._meta.get_field('short_text').verbose_name = 'Краткое описание статьи'
Article._meta.get_field('text').verbose_name = 'Содержание статьи'
