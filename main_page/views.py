from django.shortcuts import render

# Create your views here.
from news.models import Article
from settings.models import Page
from .models import MainSlider, SecondarySlider, SingleBlock, Review


def main_view(request):
    page = Page.objects.get(name="index")

    main_slides = MainSlider.objects.all()

    secondary_slides = SecondarySlider.objects.filter(active=True)

    single_block = SingleBlock.objects.all().first()

    news = Article.objects.filter(status="published").order_by("-date")[:2]

    reviews = Review.objects.filter(active=True, language=request.LANGUAGE_CODE)[:10]

    context = {
        "page": page,
        "main_slides": main_slides,
        "secondary_slides": secondary_slides,
        "single_block": single_block,
        "news": news,
        "reviews": reviews,
        "data_offset": "['210','100','100','100']" if request.LANGUAGE_CODE == "ru" else "['270','150','140','120']"  # Width of additional button
    }
    return render(request, "main_page/index.html", context)
