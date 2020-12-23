from modeltranslation.translator import register, TranslationOptions
from .models import MainSlider, SecondarySlider, SingleBlock, StaticBlock

@register(MainSlider)
class MainSliderTranslationOptions(TranslationOptions):
    fields = ("title", "text")

@register(SecondarySlider)
class SecondarySliderTranslationOptions(TranslationOptions):
    fields = ("title", "text")

@register(SingleBlock)
class SingleBlockTranslationOptions(TranslationOptions):
    fields = ("title", "text")

@register(StaticBlock)
class StaticBlockTranslationOptions(TranslationOptions):
    fields = ("title", "text")
