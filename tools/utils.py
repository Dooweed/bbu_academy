from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from easy_thumbnails.files import get_thumbnailer


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

def link_tag(url, name=None, classes=None):
    if not name:
        name = url
    return f"""<a href="{url}"{"" if not classes else " ".join(classes)}>{name}</a>"""

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
