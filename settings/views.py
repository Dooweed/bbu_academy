from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from bbu_academy.settings import ADMIN_EMAIL
from settings.models import Page
from django.views.generic import View
from django.urls import resolve
from .forms import MessageForm

# Create your views here.

def contacts(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            user_email = form.cleaned_data.get("email")
            context = {
                "name": name,
                "email": user_email,
                "subject": form.cleaned_data.get("subject"),
                "message": form.cleaned_data.get("message"),
            }
            rendered_message = render_to_string('contacts/email_message.html', context)

            send_mail(
                subject=f"Новое сообщение от {name} с сайта {request.get_host()}",
                message=strip_tags(rendered_message),
                from_email=user_email,
                recipient_list=[ADMIN_EMAIL, ],
                fail_silently=True,
                html_message=rendered_message
            )
            form = MessageForm()
    else:
        form = MessageForm()

    page = Page.objects.get(name="contacts")
    context = {
        "page": page,
        "form": form
    }
    return render(request, "contacts/contacts.html", context)

class Static(View):
    def get(self, request):
        page = get_object_or_404(Page, name=resolve(request.path_info).url_name)
        return render(request, page.template_name, {"page": page})


def handler404(request, *args, **kwargs):
    return render(request, "errors/error_404.html", status=404)

def handler500(request, *args, **kwargs):
    return render(request, "errors/error_500.html", status=500)
