import qrcode
import pdfkit
from PIL import Image
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
# import time

from .forms import RegistryForm
from .models import Certificate
from settings.models import Page

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

def qr_code(request, inn: int):
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
        response = HttpResponse(content_type='image/jpg')
        img_qr_big.save(response, "JPEG")
        response['Content-Disposition'] = 'attachment; filename="qr.jpg"'
    except Exception:
        raise Http404
    return response

def download_pdf_certificate(request, inn: int):
    path_wkhtmltopdf = r'static\wkhtmltox\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    # start = time.time()
    certificate = Certificate.objects.filter(inn=inn)
    # end = time.time()
    # print(f"DATABASE QUERY - Time spent: {int((end-start)*1000)}ms {int((end-start)*1000000)}mks {int((end-start)*1000000000)}ns")
    if certificate.exists():
        context = {
            "certificate": certificate.first(),
            "pdf": True,
            "request": request
        }
        # start = time.time()
        html = render_to_string('registry/download_certificate_wrap.html', context)
        # end = time.time()
        # print(f"RENDERING TEMPLATE - Time spent: {int((end-start)*1000)}ms {int((end-start)*1000000)}mks {int((end-start)*1000000000)}ns")

        options = {
            'quiet': ''
        }
        # start = time.time()
        pdf = pdfkit.from_string(
            html,
            False,
            configuration=config,
            options=options
        )
        # end = time.time()
        # print(f"Creating pdf: Time spent: {int((end-start)*1000)}ms {int((end-start)*1000000)}mks {int((end-start)*1000000000)}ns")
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="certificate-{inn}.pdf"'
        return response
    else:
        raise Http404("Запрошенный сертификат не существует")

