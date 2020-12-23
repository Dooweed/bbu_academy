from django.shortcuts import render

# Create your views here.
from settings.models import Page
from .models import MainSlider, SecondarySlider, SingleBlock, StaticBlock, Review


def main_view(request):
    page = Page.objects.get(name="index")

    slides = MainSlider.objects.all()
    if slides.exists():
        main_slide1 = slides[0]
        main_slide2 = slides[1]
    else:
        main_slide1 = None
        main_slide2 = None

    secondary_slides = SecondarySlider.objects.filter(active=True)

    single_block = SingleBlock.objects.all().first()

    static_blocks = StaticBlock.objects.filter(active=True)

    reviews = Review.objects.filter(active=True, language=request.LANGUAGE_CODE)[:10]

    context = {
        "page": page,
        "main_slide1": main_slide1,
        "main_slide2": main_slide2,
        "secondary_slides": secondary_slides,
        "single_block": single_block,
        "static_blocks": static_blocks,
        "reviews": reviews,
    }
    return render(request, "main_page/index.html", context)
