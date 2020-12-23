from django.template.loader import render_to_string
from django import template
from django.utils.translation import gettext as _

from ..models import Article

register = template.Library()

@register.simple_tag
def courses_sidebar():
    NUMBER_OF_NEWS = 3

    courses = Article.objects.filter(status="published")[:NUMBER_OF_NEWS]

    context = {
        "courses": courses,
    }

    return render_to_string("courses/courses_sidebar.html", context) if courses.exists() else ""

@register.simple_tag
def recent_news(current_id=None, bg_color="#FFF"):
    news = Article.objects.filter(status="published")
    if current_id is not None:
        news = news.exclude(id=current_id)
        slider_title = _("Читайте также")
    else:
        slider_title = _("Свежие новости")
    news = news[:4]

    context = {
        "slider_title": slider_title,
        "news": news,
        "bg_color": bg_color,
        "unique_id": "recent"
    }

    return render_to_string("news/news_slider.html", context) if news.exists() else ""

@register.simple_tag
def category_news(current_id, category, bg_color="#FFF"):
    if not category:
        return ""

    news = Article.objects.filter(status="published", category__name=category).exclude(id=current_id)[:4]

    context = {
        "slider_title": _(f"Ещё новости из категории \"{category}\""),
        "news": news,
        "bg_color": bg_color,
        "unique_id": "category"
    }

    return render_to_string("news/news_slider.html", context) if news.exists() else ""
