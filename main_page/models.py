from django.db import models
# Create your models here.
from django.urls import reverse

from bbu_academy.settings import LANGUAGES
from courses.models import Course
from news.models import Article
from settings.models import StaticInformation
from tools.image_mixin import ImageMixin
from trainings.models import Training

REFERENCE_CHOICES = (
    ("news_reference", "Новости"),
    ("training_reference", "Тренинги"),
    ("course_reference", "Курсы"),
)
BUTTON_CHOICES = (
    (None, "Без дополнительной кнопки"),
    ("call", "Кнопка \"Позвонить\""),
    ("contact", "Ссылка на страницу \"Контакты\"")
)
RATING_CHOICES = (
    (0, "☆☆☆☆☆"),
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
)

class MainSlider(models.Model):
    title = models.CharField("Заголовок", help_text="Оставьте поле пустым, чтобы использовать заголовок выбранной записи", max_length=100, null=True, blank=True)
    text = models.CharField("Текст", help_text="Оставьте поле пустым, чтобы использовать текст выбранной записи", max_length=250, null=True, blank=True)

    reference = models.CharField("Привязка к разделу", choices=REFERENCE_CHOICES, help_text="Выберите раздел, к которому будет привязан слайд", max_length=30,
                                 default="news_reference")
    news_reference = models.ForeignKey(verbose_name="Выберите новость", help_text="Выберите статью, на которую будет ссылаться данный слайд", to=Article,
                                       on_delete=models.DO_NOTHING, null=True, blank=True)
    training_reference = models.ForeignKey(verbose_name="Выберите тренинг", help_text="Выберите тренинг, на который будет ссылаться данный слайд", to=Training,
                                           on_delete=models.DO_NOTHING, null=True, blank=True)
    course_reference = models.ForeignKey(verbose_name="Выберите курс", help_text="Выберите курс, на который будет ссылаться данный слайд", to=Course,
                                         on_delete=models.DO_NOTHING, null=True, blank=True)

    button = models.CharField("Дополнительная кнопка", choices=BUTTON_CHOICES, default=None, max_length=100, null=True, blank=True)
    sorting = models.PositiveIntegerField("Порядок отображения в слайдере", default=0, blank=False, null=False)

    def __str__(self):
        return self.name()

    def name(self):
        return f"Слайд #{self.sorting+1}"
    name.short_description = "Название"

    def get_key(self):
        if self.reference == "news_reference":
            return self.news_reference
        elif self.reference == "training_reference":
            return self.training_reference
        elif self.reference == "course_reference":
            return self.course_reference

    def get_title(self):
        if self.title:
            return self.title
        elif self.get_key():
            return self.get_key().title
        else:
            return super().__str__()
    get_title.short_description = "Заголовок"

    def get_text(self):
        if self.text:
            return self.text
        elif self.get_key():
            return self.get_key().short_description()

    def has_button(self):
        return self.button is not None

    def get_button_action(self):
        if self.button == "call":
            phone1 = StaticInformation.objects.get(key="phone1")
            return f"tel:{phone1.value}"
        elif self.button == "contact":
            return reverse("contacts")
        else:
            return ""

    def get_button_text(self):
        if self.button == "call":
            return "Позвонить"
        elif self.button == "contact":
            return "Написать"

    def get_link(self):
        if self.reference == "news_reference":
            return reverse("news:article", args=[self.news_reference.url])
        elif self.reference == "training_reference":
            return reverse("trainings:training", args=[self.training_reference.url])
        elif self.reference == "course_reference":
            return reverse("courses:course", args=[self.course_reference.url])

    class Meta:
        ordering = ['sorting']
        verbose_name = "Элемент карусели"
        verbose_name_plural = "Элементы карусели"

class SecondarySlider(models.Model):
    title = models.CharField("Заголовок", help_text="Оставьте поле пустым, чтобы использовать заголовок выбранной записи", max_length=100, null=True, blank=True)
    text = models.CharField("Текст", help_text="Оставьте поле пустым, чтобы использовать текст выбранной записи", max_length=150, null=True, blank=True)
    active = models.BooleanField("Активно", help_text="Неактивные слайды не будут отображены в слайдере", default=True)

    reference = models.CharField("Привязка к разделу", choices=REFERENCE_CHOICES, help_text="Выберите раздел, к которому будет привязан слайд", max_length=30,
                                 default="news_reference")
    news_reference = models.ForeignKey(verbose_name="Выберите новость", help_text="Выберите статью, на которую будет ссылаться данный слайд", to=Article,
                                       on_delete=models.DO_NOTHING, null=True, blank=True)
    training_reference = models.ForeignKey(verbose_name="Выберите тренинг", help_text="Выберите тренинг, на который будет ссылаться данный слайд", to=Training,
                                           on_delete=models.DO_NOTHING, null=True, blank=True)
    course_reference = models.ForeignKey(verbose_name="Выберите курс", help_text="Выберите курс, на который будет ссылаться данный слайд", to=Course,
                                         on_delete=models.DO_NOTHING, null=True, blank=True)

    sorting = models.PositiveIntegerField("Порядок отображения в слайдере", default=0, blank=False, null=False)

    def __str__(self):
        return self.get_title()

    def get_key(self):
        if self.reference == "news_reference":
            return self.news_reference
        elif self.reference == "training_reference":
            return self.training_reference
        elif self.reference == "course_reference":
            return self.course_reference

    def get_title(self):
        if self.title:
            return self.title
        elif self.get_key():
            return self.get_key().short_title()
        else:
            return super().__str__()
    get_title.short_description = "Заголовок"

    def get_text(self):
        if self.text:
            return self.text
        elif self.get_key():
            return self.get_key().extra_short_description()

    def get_link(self):
        if self.reference == "news_reference":
            return reverse("news:article", args=[self.news_reference.url])
        elif self.reference == "training_reference":
            return reverse("trainings:training", args=[self.training_reference.url])
        elif self.reference == "course_reference":
            return reverse("courses:course", args=[self.course_reference.url])

    class Meta:
        ordering = ['sorting']
        verbose_name = "Элемент слайдера"
        verbose_name_plural = "Элементы слайдера"

class SingleBlock(models.Model):
    title = models.CharField("Заголовок", help_text="Оставьте поле пустым, чтобы использовать заголовок выбранной записи", max_length=100, null=True, blank=True)
    text = models.CharField("Текст", help_text="Оставьте поле пустым, чтобы использовать текст выбранной записи", max_length=150, null=True, blank=True)

    reference = models.CharField("Привязка к разделу", choices=REFERENCE_CHOICES, help_text="Выберите раздел, к которому будет привязан данный блок", max_length=30,
                                 default="news_reference")
    news_reference = models.ForeignKey(verbose_name="Выберите новость", help_text="Выберите статью, на которую будет ссылаться данный блок", to=Article,
                                       on_delete=models.DO_NOTHING, null=True, blank=True)
    training_reference = models.ForeignKey(verbose_name="Выберите тренинг", help_text="Выберите тренинг, на который будет ссылаться данный блок", to=Training,
                                           on_delete=models.DO_NOTHING, null=True, blank=True)
    course_reference = models.ForeignKey(verbose_name="Выберите курс", help_text="Выберите курс, на который будет ссылаться данный блок", to=Course,
                                         on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.get_title()

    def get_key(self):
        if self.reference == "news_reference":
            return self.news_reference
        elif self.reference == "training_reference":
            return self.training_reference
        elif self.reference == "course_reference":
            return self.course_reference

    def get_title(self):
        if self.title:
            return self.title
        elif self.get_key():
            return self.get_key().title
        else:
            return super().__str__()
    get_title.short_description = "Заголовок"

    def get_text(self):
        if self.text:
            return self.text
        elif self.get_key():
            return self.get_key().short_description()

    def get_link(self):
        if self.reference == "news_reference":
            return reverse("news:article", args=[self.news_reference.url])
        elif self.reference == "training_reference":
            return reverse("trainings:training", args=[self.training_reference.url])
        elif self.reference == "course_reference":
            return reverse("courses:course", args=[self.course_reference.url])

    class Meta:
        verbose_name = "Одиночный блок"
        verbose_name_plural = "Одиночный блок"


class StaticBlock(models.Model):
    title = models.CharField("Заголовок", help_text="Оставьте поле пустым, чтобы использовать заголовок выбранной записи", max_length=100, null=True, blank=True)
    text = models.CharField("Текст", help_text="Оставьте поле пустым, чтобы использовать текст выбранной записи", max_length=150, null=True, blank=True)
    active = models.BooleanField("Активно", help_text="Неактивные слайды не будут отображены в слайдере", default=True)

    reference = models.CharField("Привязка к разделу", choices=REFERENCE_CHOICES, help_text="Выберите раздел, к которому будет привязан данный блок", max_length=30,
                                 default="news_reference")
    news_reference = models.ForeignKey(verbose_name="Выберите новость", help_text="Выберите статью, на которую будет ссылаться данный блок", to=Article,
                                       on_delete=models.DO_NOTHING, null=True, blank=True)
    training_reference = models.ForeignKey(verbose_name="Выберите тренинг", help_text="Выберите тренинг, на который будет ссылаться данный блок", to=Training,
                                           on_delete=models.DO_NOTHING, null=True, blank=True)
    course_reference = models.ForeignKey(verbose_name="Выберите курс", help_text="Выберите курс, на который будет ссылаться данный блок", to=Course,
                                         on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.get_title()

    def get_key(self):
        if self.reference == "news_reference":
            return self.news_reference
        elif self.reference == "training_reference":
            return self.training_reference
        elif self.reference == "course_reference":
            return self.course_reference

    def has_image(self):
        if self.get_key() is None:
            return None
        else:
            return self.get_key().has_image()

    def get_title(self):
        if self.title:
            return self.title
        elif self.get_key():
            return self.get_key().short_title()
        else:
            return super().__str__()
    get_title.short_description = "Заголовок"

    def get_text(self):
        if self.text:
            return self.text
        elif self.get_key():
            return self.get_key().short_description()

    def get_link(self):
        if self.reference == "news_reference":
            return reverse("news:article", args=[self.news_reference.url])
        elif self.reference == "training_reference":
            return reverse("trainings:training", args=[self.training_reference.url])
        elif self.reference == "course_reference":
            return reverse("courses:course", args=[self.course_reference.url])

    class Meta:
        verbose_name = "Статичный блок"
        verbose_name_plural = "Статичные блоки"


class Review(ImageMixin):
    name = models.CharField("Имя", max_length=200)
    status = models.CharField("Статус (ученик, сотрудник, ...)", max_length=70)
    active = models.BooleanField("Активно", help_text="Неактивные слайды не будут отображены в слайдере", default=True)
    rating = models.IntegerField("Оценка", choices=RATING_CHOICES, default=5)
    language = models.CharField("Язык комментария", choices=LANGUAGES, max_length=20)

    image = models.ImageField("Аватар", upload_to="reviews/", null=True, blank=True)

    text = models.CharField("Содержание комментария", max_length=750)
    sorting = models.PositiveIntegerField("Порядок отображения в слайдере", default=0, blank=False, null=False)

    def __str__(self):
        return f"Комментарий от {self.name}"

    def rating_classes(self):
        classes = []
        for i in range(0, 5):
            classes.append("on" if i < self.rating else "off")
        return classes

    class Meta:
        ordering = ['sorting']
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
