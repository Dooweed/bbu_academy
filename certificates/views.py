import os
from pathlib import Path

import qrcode
import pdfkit
from PIL import Image
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from bbu_academy.settings import BASE_DIR
from .forms import RegistryForm
from .models import Certificate
from settings.models import Page
from django.conf import settings

# Create your views here.

def registry_view(request):
    context = {}
    if 'inn' in request.GET:
        inn = Certificate.objects.filter(inn=request.GET.get('inn'))
        if inn.exists():
            return render(request, "registry/certificate_wrap.html", {"certificate": inn.first()})
        else:
            context['not_found'] = True
    form = RegistryForm()
    page = get_object_or_404(Page, name="registry:registry")

    context["page"] = page
    context["form"] = form

    return render(request, page.template_name, context)

def qr_code(request, inn: int, only_image=False):
    try:
        logo = Image.open('static/images/logo.png')
        width = 150
        size = (width, int(logo.size[1]/(logo.size[0]/width)))
        logo = logo.resize(size)
        background = Image.new("RGB", size, (255, 255, 255))
        background.paste(logo, logo)
        logo = background

        qr_big = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H
        )

        qr_big.add_data(f"{request.get_host()}{reverse('registry:certificate')}?inn={inn}")
        qr_big.make()
        img_qr_big = qr_big.make_image(fill_color="#0D2969").convert('RGB')

        pos = ((img_qr_big.size[0] - logo.size[0]) // 2, (img_qr_big.size[1] - logo.size[1]) // 2)

        img_qr_big.paste(logo, pos)

        if only_image:
            return img_qr_big

        response = HttpResponse(content_type='image/jpg')
        img_qr_big.save(response, "JPEG")
        response['Content-Disposition'] = 'attachment; filename="qr.jpg"'
    except Exception:
        raise Http404()
    return response

def download_pdf_certificate(request, inn: int):
    config = pdfkit.configuration(wkhtmltopdf=settings.PATH_WKHTMLTOPDF)

# file:///home/wwwtcatb/bbu_academy
    certificate = Certificate.objects.filter(inn=inn)

    if certificate.exists():
        # Get QR image
        qr_name = f"{inn}.jpg"
        qr_path = Path("media") / "temp" / "qr"
        qr_path.mkdir(parents=True, exist_ok=True)
        qr = qr_code(request, inn, True)
        qr.save(BASE_DIR / qr_path / qr_name, "JPEG")

        # Render template
        print(f"{reverse('registry:certificate')}?inn={inn}")
        context = {
            "certificate": certificate.first(),
            "pdf": True,
            "qr_name": qr_name,
            "FILE_BASE_DIR": settings.BASE_DIR,
            "link": f"{request.build_absolute_uri(reverse('registry:certificate'))}?inn={inn}",
            "request": request,
        }
        html = render_to_string('registry/download_certificate_wrap.html', context)

        # Define pdf options
        options = {
            'images': '',
            'enable-local-file-access': '',
            'enable-external-links': '',
            'enable-internal-links': '',
            'resolve-relative-links': '',
            'load-media-error-handling': 'skip',
            # 'quiet': '',
        }

        # Create pdf
        pdf = pdfkit.from_string(
            html,
            False,
            configuration=config,
            options=options,
        )

        # Remove QR image
        os.remove(qr_path / qr_name)

        # Prepare response
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="certificate-{inn}.pdf"'
        return response
    else:
        raise Http404("Запрошенный сертификат не существует")

