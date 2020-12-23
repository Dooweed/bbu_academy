from django import template
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from ..models import Course

register = template.Library()
@register.simple_tag
def courses_sidebar():
    NUMBER_OF_COURSES = 3

    courses = Course.objects.filter(active=True)[:NUMBER_OF_COURSES]

    context = {
        "courses": courses,
    }

    return render_to_string("chunks/../../templates/courses/courses_sidebar.html", context) if courses.exists() else ""

@register.simple_tag
def other_courses(current_id=None, bg_color="#FFF"):
    NUMBER_OF_COURSES = 4
    courses = Course.objects.filter(active=True)
    if current_id is not None:
        courses = courses.exclude(id=current_id)
        slider_title = _("У нас есть и другие курсы")
    else:
        slider_title = _("Попробуйте наши курсы")
    courses = courses[:NUMBER_OF_COURSES]

    context = {
        "courses": courses,
        "slider_title": slider_title,
        "bg_color": bg_color,
        "unique_id": "other"
    }

    return render_to_string("chunks/../../templates/courses/courses_slider.html", context) if courses.exists() else ""
