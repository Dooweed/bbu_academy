from django import template
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from ..models import Service

register = template.Library()
@register.simple_tag
def services_sidebar():
    NUMBER_OF_SERVICES = 3

    services = Service.objects.filter(active=True)[:NUMBER_OF_SERVICES]

    context = {
        "services": services,
    }

    return render_to_string("services/services_sidebar.html", context) if services.exists() else ""

@register.simple_tag
def other_services(current_id=None, bg_color="#FFF"):
    NUMBER_OF_ITEMS = 4
    services = Service.objects.filter(active=True)
    if current_id is not None:
        services = services.exclude(id=current_id)
        slider_title = _("У нас есть и другие услуги")
    else:
        slider_title = _("Попробуйте наши услуги")
    services = services[:NUMBER_OF_ITEMS]

    context = {
        "services": services,
        "slider_title": slider_title,
        "bg_color": bg_color,
        "unique_id": "other"
    }

    return render_to_string("services/services_slider.html", context) if services.exists() else ""
