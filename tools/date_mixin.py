from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.utils.translation import gettext as _

from tools.utils import get_ending

# Translators: Примеры: 2 января, Четырнадцатого марта
MONTHS = (_("января"), _("февраля"), _("марта"), _("апреля"), _("мая"), _("июня"), _("июля"), _("августа"), _("сентября"), _("октября"), _("ноября"), _("декабря"))

# Translators: Пример: 1 час назад
HOUR_BEFORE = _('час назад')
# Translators: Пример: 2 часа назад
HOURS_BEFORE = _('часа назад')
# Translators: Пример: 6 часов назад
HOURS_BEFORE_2 = _('часов назад')

class DateMixin(models.Model):
    date = models.DateTimeField("Дата создания")

    def date_string(self):
        if timezone.now().year == self.date.year:
            if self.date > timezone.now() - timedelta(days=1):
                hours = round((timezone.now() - self.date).seconds/3600)
                if hours == 0:
                    return _("менее часа назад")
                else:
                    return get_ending(hours, (HOUR_BEFORE, HOURS_BEFORE, HOURS_BEFORE_2))
            else:
                date_string = self.date.strftime("%d {}")
                return date_string.format(MONTHS[self.date.month-1])
        else:
            date_string = self.date.strftime("%d {} %Y")
            return date_string.format(MONTHS[self.date.month-1])

    class Meta:
        abstract = True
