from django.db import ProgrammingError
from django.utils.translation import gettext as _

from purchase.models import PurchaseRecord
from trainings.models import Training
from courses.models import Course

def get_product_choices():
    try:
        courses = Course.objects.filter(active=True)
        trainings = Training.objects.filter(active=True)

        choices = []

        for item in courses:
            choices.append((f"course-{item.id}", _("Курс: ") + f"{item.title} ({item.f_price()} {_('сум')})"))

        for item in trainings:
            choices.append((f"training-{item.id}", _("Тренинг: ") + f"{item.title} ({item.f_price()} {_('сум')})"))

        return tuple(choices)
    except ProgrammingError:
        print("get_product_choices() from purchase.utils produced ProgrammingError. Skip this message if it was running of 'makemigrations' command")
        return []

def delete_session_purchase_record(request):
    try:
        if "record_id" in request.session:
            record = PurchaseRecord.objects.filter(id=request.session["record_id"])
            if record.exists():
                record.delete()
            del request.session["record_id"]
            request.session.modified = True
    except ProgrammingError:
        print("delete_session_purchase_record() from purchase.utils produced ProgrammingError. Skip this message if it was running of 'makemigrations' command")
        return []
