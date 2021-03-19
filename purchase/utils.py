from base64 import b64decode

import pdfkit
from django.core.files.storage import default_storage
from django.db import ProgrammingError, OperationalError
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from bbu_academy.settings import PATH_WKHTMLTOPDF, BASE_DIR
from purchase.models import PurchaseRecord
from trainings.models import Training
from courses.models import Course

def get_product_choices():
    try:
        courses = Course.objects.filter(active=True)
        trainings = Training.objects.filter(active=True)

        choices = [(None, '---------')]

        for item in courses:
            choices.append((f"course-{item.id}", _("Курс: ") + f"{item.title} ({item.f_price()} {_('сум')})"))

        for item in trainings:
            choices.append((f"training-{item.id}", _("Тренинг: ") + f"{item.title} ({item.f_price()} {_('сум')})"))

        return tuple(choices)
    except ProgrammingError:
        print("get_product_choices() from purchase.utils produced ProgrammingError. Skip this message if it happened during running 'makemigrations' command")
        return []
    except OperationalError:  # SQLite error
        print("get_product_choices() from purchase.utils produced OperationalError. Skip this message if it happened during running 'makemigrations' command")
        return []

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

def build_invoice(record, request):
    config = pdfkit.configuration(wkhtmltopdf=PATH_WKHTMLTOPDF)

    context = {
        "record": record,
        "FILE_BASE_DIR": BASE_DIR,
    }
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
