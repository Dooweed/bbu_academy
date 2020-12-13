from django.db import models
from django.shortcuts import reverse

# Create your models here.

class Page(models.Model):
    name = models.CharField("Имя страницы (из urls.py)", max_length=200, unique=True)
    template_name = models.CharField("Путь к шаблону", max_length=200, null=True, blank=True)
    parent_page = models.ForeignKey(verbose_name="Следует после (в хлебных крошках)", to='Page', on_delete=models.DO_NOTHING, null=True, blank=True)
    sorting = models.PositiveIntegerField("Порядок отображения в меню", default=0, blank=False, null=False)
    title = models.CharField("Заголовок страницы", max_length=200)
    show_in_menu = models.BooleanField("Показывать в меню", default=False)
    menu_name = models.CharField("Название в меню", help_text="Оставьте пустым, чтобы использовать заголовок страницы", max_length=200, null=True, blank=True)
    meta_description = models.CharField("Описание (мета-тег)", help_text="Необязательно. Используется для SEO.", max_length=1000, null=True, blank=True)
    meta_keywords = models.CharField("Ключевые слова (мета-тег)", help_text="Необязательно. Используется для SEO.", max_length=500, null=True, blank=True)
    meta_robots = models.CharField("Robots (мета-тег)", help_text="Необязательно. Используется для SEO.", max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_menu_name(self):
        return self.menu_name if self.menu_name else self.title

    def breadcrumbs(self, first_call=True):
        if first_call:
            this_value = f"""<li class="active">{self.title}</li>"""
        else:
            this_value = f"""<li><a href="{reverse(self.name)}" title="{self.title}">{self.title}</a></li>"""
        if self.parent_page:
            return f"{self.parent_page.breadcrumbs(False)}\n{this_value}"
        else:
            return this_value

    class Meta:
        ordering = ['sorting']
        verbose_name = "Настройки страницы"
        verbose_name_plural = "Настройки страниц"

class StaticInformation(models.Model):
    name = models.CharField("Название", max_length=200)
    key = models.CharField("Ключ", max_length=200)
    value = models.CharField("Значение", max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статическая информация"
        verbose_name_plural = "Статическая информация"
