from django import template
from django.template.loader import render_to_string

from ..models import Training

register = template.Library()
@register.simple_tag
def trainings_sidebar():
    NUMBER_OF_COURSES = 3

    trainings = Training.objects.filter(active=True)[:NUMBER_OF_COURSES]

    context = {
        "trainings": trainings,
    }

    return render_to_string("trainings/trainings_sidebar.html", context) if trainings.exists() else ""
