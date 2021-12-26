from django.shortcuts import render, get_object_or_404

from settings.models import Page
from .models import Service


def services_list_view(request):
    page = get_object_or_404(Page, name="services:services")
    services = Service.objects.filter(active=True)[:10]

    context = {
        "services": services,
        "page": page
    }
    return render(request, 'services/services.html', context)

def service_view(request, service_url):
    page = get_object_or_404(Page, name="services:service")
    service = get_object_or_404(Service, url=service_url, active=True)

    request.session["product_class"] = "Service"
    request.session["product_id"] = service.id

    context = {
        "service": service,
        "page": page
    }
    return render(request, 'services/service.html', context)
