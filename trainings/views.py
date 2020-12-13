from django.shortcuts import render, get_object_or_404

# Create your views here.
from settings.models import Page
from .models import Training


def trainings_list_view(request):
    page = get_object_or_404(Page, name="trainings:trainings")
    trainings = Training.objects.filter(active=True)[:10]

    context = {
        "trainings": trainings,
        "page": page
    }
    return render(request, 'trainings/trainings.html', context)

def training_view(request, training_url):
    page = get_object_or_404(Page, name="trainings:training")
    training = get_object_or_404(Training, url=training_url, active=True)

    context = {
        "training": training,
        "page": page
    }
    return render(request, 'trainings/training.html', context)
