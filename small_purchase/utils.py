from django.db import ProgrammingError, OperationalError
from django.utils.translation import gettext as _

from services.models import Service
from trainings.models import Training


def get_product_choices():
    try:
        services = Service.objects.filter(active=True)
        trainings = Training.objects.filter(active=True)

        choices = [(None, '---------')]
        appendix = "(" + str(_('Онлайн: ')) + "{online}" + "/" + str(_('Офлайн: ')) + "{offline}" + ")"
        for item in services:
            choices.append((f"course-{item.id}", _('Услуга: ') + item.title + appendix.format(online=item.online_beautified_price(), offline=item.offline_beautified_price())))

        for item in trainings:
            choices.append((f"training-{item.id}", _("Тренинг: ") + item.title + appendix.format(online=item.online_beautified_price(), offline=item.offline_beautified_price())))

        return tuple(choices)
    except ProgrammingError:
        print("get_product_choices() from purchase.utils produced ProgrammingError. Skip this message if it happened during running 'makemigrations' command")
        return []
    except OperationalError:  # SQLite error
        print("get_product_choices() from purchase.utils produced OperationalError. Skip this message if it happened during running 'makemigrations' command")
        return []
