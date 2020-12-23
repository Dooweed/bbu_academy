from django.db import models
from django.utils.html import strip_tags


class DescriptionMixin(models.Model):
    DESCRIPTION_LENGTH = 500
    SHORT_DESCRIPTION_LENGTH = 250
    EXTRA_SHORT_DESCRIPTION_LENGTH = 120
    META_DESCRIPTION_LENGTH = 250

    short_text = models.CharField("Описание", help_text=f"Информация для превью (необязательно). Оставьте поле пустым, чтобы использовать первые {DESCRIPTION_LENGTH} знаков статьи",
                                  max_length=DESCRIPTION_LENGTH, null=True, blank=True)
    meta_description = models.CharField("Описание (мета-тег)", help_text=f"Оставьте поле пустым, чтобы использовать первые {META_DESCRIPTION_LENGTH} знаков статьи",
                                        max_length=META_DESCRIPTION_LENGTH, null=True, blank=True)
    text = models.TextField("Контент")

    def extra_short_description(self):
        return self.description(self.EXTRA_SHORT_DESCRIPTION_LENGTH)

    def short_description(self):
        return self.description(self.SHORT_DESCRIPTION_LENGTH)

    def description(self, length=DESCRIPTION_LENGTH):
        if self.short_text:
            return strip_tags(self.short_text)[:length] + "..."
        else:
            short_text = strip_tags(self.text[:length * 2])[:length]
            index = short_text.rfind(" ")
            if index == -1:
                return f"{short_text}..."
            else:
                return f"{short_text[:index]}..."

    def get_meta_description(self):
        return self.meta_description if self.meta_description else strip_tags(self.text[:self.META_DESCRIPTION_LENGTH*2])[:self.META_DESCRIPTION_LENGTH]

    def set_short_text_verbose(self, short_text_verbose):
        self.short_text.verbose_name = short_text_verbose

    def set_meta_description_verbose(self, meta_description_verbose):
        self.meta_description.verbose_name = meta_description_verbose

    def set_text_verbose(self, text_verbose):
        self.text.verbose_name = text_verbose

    class Meta:
        abstract = True
