from django import template

from purchase.models import EDUCATION

register = template.Library()

@register.simple_tag()
def verbose_education(key):
    for item in EDUCATION:
        if item[0] == key:
            return item[1]
