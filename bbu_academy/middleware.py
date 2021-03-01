from django.conf.global_settings import LANGUAGE_COOKIE_NAME
from django.http import HttpResponseForbidden

from django.utils import translation

from django.utils.translation import gettext as _


class LanguageBasedOnUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = "ru"

        if request.path.startswith("/admin"):
            translation.activate(language)

        response = self.get_response(request)

        if request.path.startswith("/admin"):
            response.set_cookie(LANGUAGE_COOKIE_NAME, language)

        return response

class DeleteUnusedPersonalFilesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # print(request.path)
        # print(vars(request.session))

        # if "/purchase/" not in request.path:
        #     clear_temp_purchase_files(request, True)

        response = self.get_response(request)

        # print(vars(request.session))
        # print()

        return response

class ProtectPersonalFilesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if "/media/temp/purchase_docs/" in request.path:
            if "record_id" in request.session and f"record_{request.session['record_id']}" in request.path:
                response = self.get_response(request)
            else:
                response = HttpResponseForbidden(_("У вас нет доступа к просмотру данного файла"))
        else:
            response = self.get_response(request)

        return response
