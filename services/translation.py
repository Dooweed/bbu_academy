from modeltranslation.translator import register, TranslationOptions
from .models import Service

@register(Service)
class TrainingTranslationOptions(TranslationOptions):
    fields = ("short_text", "meta_description", "text", "title")
