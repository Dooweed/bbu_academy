from modeltranslation.translator import register, TranslationOptions
from .models import MainSlider, SecondarySlider, SingleBlock

@register(MainSlider)
class MainSliderTranslationOptions(TranslationOptions):
    fields = ("title", "text")

@register(SecondarySlider)
class SecondarySliderTranslationOptions(TranslationOptions):
    fields = ("title", "text")

@register(SingleBlock)
class SingleBlockTranslationOptions(TranslationOptions):
    fields = ("title", "text")
