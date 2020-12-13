from django.shortcuts import render, get_object_or_404

from .models import Article
from settings.models import Page


def news_list_view(request):
    page = Page.objects.get(name="news:news")
    news = list(Article.objects.filter(status="published")[:10])

    # news.sort(key=lambda article: article.has_image(), reverse=True)

    context = {
        "page": page,
        "news": news
    }

    return render(request, "news/news.html", context)


def article_view(request, article_url):
    page = Page.objects.get(name="news:article")
    article = get_object_or_404(Article, url=article_url)
    next_article = Article.objects.filter(date__gt=article.date).order_by("date").first()
    prev_article = Article.objects.filter(date__lt=article.date).first()

    page.meta_description = article.get_meta_description()

    context = {
        "page": page,
        "article": article,
        "next_article": next_article,
        "prev_article": prev_article,
    }
    return render(request, "news/article.html", context)
