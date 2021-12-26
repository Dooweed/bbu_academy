"""bbu_academy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, register_converter

from settings import views as other_views
from main_page.views import main_view
from django.conf import settings
from django.conf.urls.static import static
from certificates.url_converters import INNConverter

register_converter(INNConverter, 'inn')

urlpatterns = [
    path('admin/', admin.site.urls, name="admin"),
    path('', main_view, name='index'),
    path('contacts/', other_views.contacts, name='contacts'),
    path('set_language/<str:language>/', other_views.set_language_view, name="set_language"),


    path('about/', other_views.Static.as_view(), name='about'),
    path('library/', other_views.Static.as_view(), name='library'),

    path('courses/', include('courses.urls'), name='courses'),
    path('trainings/', include('trainings.urls'), name='trainings'),
    path('services/', include('services.urls'), name='services'),
    path('news/', include('news.urls'), name="news"),
    path('registry/', include('certificates.urls'), name="registry"),
    path('purchase/', include('purchase.urls'), name='purchase'),
    path('s-purchase/', include('small_purchase.urls'), name='small_purchase'),

    # Package urls
    url(r'^front-edit/', include('front.urls')),

    # Payment urls
    path('payme-billing/', include('payme_billing.urls'), name="uzpayments"),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = other_views.handler404
handler500 = other_views.handler500
