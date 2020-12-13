from django.template.defaultfilters import register


@register.filter
def modulo(num, val):
    return num % val
