from django.utils import timezone
from datetime import timedelta
from django.db import models

from tools.utils import get_ending

MONTHS = ("января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря")

class DateMixin(models.Model):
    date = models.DateTimeField("Дата создания")

    def date_string(self):
        if timezone.now().year == self.date.year:
            if self.date > timezone.now() - timedelta(days=1):
                hours = round((timezone.now() - self.date).seconds/3600)
                if hours == 0:
                    return "менее часа назад"
                else:
                    return f"{get_ending(hours, ('час', 'часа', 'часов'))} назад"
            else:
                date_string = self.date.strftime("%d {}")
                return date_string.format(MONTHS[self.date.month-1])
        else:
            date_string = self.date.strftime("%d {} %Y")
            return date_string.format(MONTHS[self.date.month-1])

    class Meta:
        abstract = True
