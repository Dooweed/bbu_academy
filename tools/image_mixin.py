from django.db import models

class ImageMixin(models.Model):
    @property
    def image(self):
        raise NotImplementedError

    def has_image(self):
        return bool(self.image)
    has_image.short_description = "Наличие изображения"
    has_image.boolean = bool(image)

    class Meta:
        abstract = True



