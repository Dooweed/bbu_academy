from modeltranslation.translator import register, TranslationOptions
from .models import Training

@register(Training)
class TrainingTranslationOptions(TranslationOptions):
    fields = ("short_text", "meta_description", "text", "title")
