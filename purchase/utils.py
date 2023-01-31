import pdfkit
import requests
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.db import ProgrammingError, OperationalError
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from bbu_academy.settings import PATH_WKHTMLTOPDF, BASE_DIR
from courses.models import Course
from trainings.models import Training

FORMFIELD_SIZE_RESTRICTION = 2**21  # 2Mb

def delete_session_purchase_record(request):
    try:
        if "record_id" in request.session:
            del request.session["record_id"]
            request.session.modified = True
    except ProgrammingError:
        print("delete_session_purchase_record() from purchase.utils produced ProgrammingError. Skip this message if it happened during running 'makemigrations' command")
        return []
    except OperationalError:  # SQLite error
        print("delete_session_purchase_record() from purchase.utils produced OperationalError. Skip this message if it happened during running 'makemigrations' command")
        return []

def build_invoice(record, request, short_form=False):
    context = {
        "record": record,
        "FILE_BASE_DIR": BASE_DIR,
    }

    config = pdfkit.configuration(wkhtmltopdf=PATH_WKHTMLTOPDF)
    if short_form:
        html = render_to_string('small_purchase/invoice/invoice.html', context, request=request)
    else:
        name_modifier = record.study_type_abbreviation()
        if record.language.lower() != "ru":
            context['name_modifier'] = record.language.upper() + " " + name_modifier
        html = render_to_string('purchase/invoice/invoice.html', context, request=request)

    # Define pdf options
    options = {
        'enable-external-links': '',
        'load-media-error-handling': 'skip',
    }

    # Create pdf
    pdf = pdfkit.from_string(
        html,
        False,
        configuration=config,
        options=options,
    )

    with open(record.invoice_path, "wb") as invoice:
        invoice.write(pdf)

def get_atb_members_list():
    ATBUZ_LINK = "http://atb.uz/chleny-atb/"
    html = requests.get(ATBUZ_LINK).content
    soup = BeautifulSoup(html, "lxml")
    table_rows = soup.find("table", {"class": "all-members"}).find("tbody").find_all("tr")
    inn_list = []
    for row in table_rows:
        inn = row.find_all("td")[-1].text
        if inn:
            inn_list.append(inn)
    return inn_list


def get_product_choices():
    try:
        courses = Course.objects.filter(active=True)

        choices = [(None, '---------')]
        appendix = "(" + str(_('Онлайн: ')) + "{online}" + "/" + str(_('Офлайн: ')) + "{offline}" + ")"
        for item in courses:
            choices.append((f"course-{item.id}", _('Курс: ') + item.title + appendix.format(online=item.online_beautified_price(), offline=item.offline_beautified_price())))

        return tuple(choices)
    except ProgrammingError:
        print("get_product_choices() from purchase.utils produced ProgrammingError. Skip this message if it happened during running 'makemigrations' command")
        return []
    except OperationalError:  # SQLite error
        print("get_product_choices() from purchase.utils produced OperationalError. Skip this message if it happened during running 'makemigrations' command")
        return []

def validate_file_2mb(value):
    print(value, value.size, value.size >= FORMFIELD_SIZE_RESTRICTION)
    if isinstance(value, ValidationError):
        raise value


    if value.size >= FORMFIELD_SIZE_RESTRICTION:
        raise ValidationError(_('Размер файла не должен превышать 2Мб'))
    else:
        return value
