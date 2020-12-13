from django.urls import reverse
from settings.models import Page, StaticInformation
from django.shortcuts import get_object_or_404


def static_information(*args):
    context = {}
    for obj in StaticInformation.objects.all():
        if "phone" in obj.key and "+" not in obj.value:
            context[obj.key] = f"+{obj.value}"
        context[obj.key] = obj.value
    return context

def page_menu(request, *args):
    menu_objects = Page.objects.filter(show_in_menu=True)
    menu = ""
    for item in menu_objects:
        rev = reverse(item.name)
        menu = f"""{menu}\n<li><a {'class="active"' if rev==request.path else f'href="{rev}"'} title="{item.title}">{item.get_menu_name()}</a></li>"""
    return {"page_menu": menu}

def index_link(*args):
    index_page = get_object_or_404(Page, name="index")
    return {"index_link": f"""<a href="{reverse(index_page.name)}" title="{index_page.title}">{index_page.get_menu_name()}</a>"""}
