import re
from datetime import datetime

import xlwt
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.templatetags.static import static
from django.utils.translation import get_language, gettext as _
from easy_thumbnails.files import get_thumbnailer

from io import BytesIO
from django.db.models import Model, QuerySet


def delete_unused_thumbnails(**kwargs):
    file = kwargs['file']
    thumbnailer = get_thumbnailer(file)
    deleted = thumbnailer.delete_thumbnails()
    print(f"Deleted {deleted} thumbnails")

def paired_range(start, stop):
    pairs = []
    for n in range(start, stop):
        pairs.append((n, n))
    return tuple(pairs)

def link_tag(url, name=None, classes=None, blank=False):
    if not name:
        name = url
    return f"""<a {'target="_blank"' if blank else ''} href="{url}" class="{"" if not classes else " ".join(classes)}">{name}</a>"""

def make_link(url, classes=None, name=None):
    val = URLValidator()
    try:
        val(url)
        return link_tag(url, classes, name)
    except ValidationError:
        return url

def get_ending(number, options):
    if len(options) != 3:
        return "Ошибка"
    number = str(number)
    last_char = int(number[-1:])
    if last_char == 1 and number[-2:] != '11':
        return f"{number} {options[0]}"
    elif 2 <= last_char <= 4 and number[-2:] != "12" and number[-2:] != "13" and number[-2:] != "14":
        return f"{number} {options[1]}"
    else:
        return f"{number} {options[2]}"


def pretty_string(value):
    if value is None or value == "":
        return "-"
    elif isinstance(value, datetime):
        return datetime.strftime(value, "%d.%m.%Y   %H:%M")
    elif isinstance(value, bool):
        return "✓" if value else "✗"
    else:
        return str(value)


def get_column_width(value) -> int:
    return max(len(item) for item in value.split('\n')) if len(value) > 4 else 4

def model_to_excel(query_set: QuerySet, field_names=None) -> BytesIO:
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Сертификаты")
    title_style = xlwt.XFStyle()
    borders = xlwt.Borders()
    borders.bottom, borders.right, borders.left = xlwt.Borders.MEDIUM, xlwt.Borders.MEDIUM, xlwt.Borders.MEDIUM
    title_style.borders = borders
    title_style.font = xlwt.easyfont(f"bold on, height {12 * 20};")
    font_style = xlwt.XFStyle()
    font_style.font = xlwt.easyfont(f"height {12 * 20};")

    attrs = {}
    model = query_set.model
    if field_names is None:
        for field in model._meta.fields:
            attrs[field] = True
    else:
        for name in field_names:
            try:
                attrs[model._meta.get_field(name)] = True
            except:
                attr = getattr(model, name)
                field_name = re.search(r"get_\w+_display", name)
                if field_name:
                    field_name = field_name.string.replace("get_", "").replace("_display", "")
                    field = model._meta.get_field(field_name)
                    attr.short_description = str(field.verbose_name if hasattr(field, 'verbose_name') else field.name)
                attrs[attr] = False
    record_list = list(query_set)

    for c, (attr, is_field) in enumerate(attrs.items()):
        if is_field:
            name = str(attr.verbose_name if hasattr(attr, 'verbose_name') else attr.name)
        else:
            name = str(attr.short_description if hasattr(attr, 'short_description') else attr.__name__)
        sheet.write(0, c, name, title_style)
        width = get_column_width(name)

        for r, record in enumerate(record_list):
            if is_field:
                value = getattr(record, attr.name)
            else:
                value = attr(record)
            value = pretty_string(value)
            sheet.write(r+1, c, value, font_style)
            width = max(get_column_width(value), width)

        sheet.col(c).width = width*440

    file = BytesIO()
    workbook.save(file)
    return file


def pinfl_help_text():
    image_url = static('images/help/pinfl_ru.jpg') if get_language() == 'ru' else static('images/help/pinfl_uz.png')
    return link_tag(image_url, classes=('text-underline',), name=_('Где я могу узнать свой ПИНФЛ?'), blank=True)

