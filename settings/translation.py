from modeltranslation.translator import register, TranslationOptions
from .models import Page

@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ("title", "meta_description", "meta_keywords", "menu_name")
