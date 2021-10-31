from . import views
from django.urls import path


app_name = "registry"

urlpatterns = [
    path('', views.registry_view, name='registry'),
    path('certificate', views.registry_view, name='certificate'),
    path('qr_code/<int:inn_or_pinfl>', views.qr_code, name="qr_code"),
    path('download_pdf_certificate/<int:inn_or_pinfl>', views.download_pdf_certificate, name="download_pdf_certificate"),
]
