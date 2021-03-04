# import requests
#
# from bbu_academy.settings import PAYME_TEST, WEB_CASH_ID, WEB_CASH_KEY, WEB_CASH_TEST_ID, WEB_CASH_TEST_KEY
#
#
# class SubscribeAPI:
#     url = "https://checkout.test.paycom.uz/api" if PAYME_TEST else "https://checkout.paycom.uz/api"
#
#     def _auth_headers(self):
#         headers = {
#             "X-Auth": f"{WEB_CASH_TEST_ID if PAYME_TEST else WEB_CASH_ID}:{WEB_CASH_TEST_KEY if PAYME_TEST else WEB_CASH_KEY}"
#         }
#         return
#
#     def create_receipt(self):
#         requests.post(url=self.url)

import json
from base64 import b64decode
from binascii import Error as BinasciiError

from .utils import Error
from .vars.settings import WEB_CASH_KEY
from .vars.static import *
from . import merchant_api_methods

available_methods = ("CheckPerformTransaction", "CreateTransaction", "PerformTransaction", "CancelTransaction", "CheckTransaction", "GetStatement")


class MerchantApiRequest:
    result = None
    request_id = None
    method = None
    params = None

    def __init__(self, request):
        if request.method != "POST":  # Check if request method is not POST
            self.result = Error(REQUEST_METHOD_ERROR)
            return

        # Check Authorization header
        if "Authorization" not in request.headers:
            self.result = Error(RIGHTS_ERROR)
            return

        # Check Authorization key
        try:
            auth = request.headers["Authorization"]
            auth = b64decode(auth.replace("Basic ", "")).decode()
            if auth.split(":")[1] != WEB_CASH_KEY:
                self.result = Error(RIGHTS_ERROR)
                return
        except BinasciiError:
            self.result = Error(RIGHTS_ERROR)
            return

        # Parse json
        content = request.POST if request.POST else json.loads(request.body)

        # Check if request content is empty
        if not content:
            self.result = Error(JSON_ERROR)
            return

        # Check whether id was present in json
        if "id" in content and isinstance(content["id"], int):
            self.request_id = content["id"]
        else:
            self.result = Error(FIELD_ERROR, "Идентификатор запроса отсутствует")
            return

        # Check whether method was present in json
        if "method" in content:
            self.method = content["method"]
        else:
            self.result = Error(FIELD_ERROR, "Метод отсутствует")
            return

        # Check whether params were present in json
        if "params" in content and isinstance(content["params"], dict):
            self.params = content["params"]
        else:
            self.result = Error(FIELD_ERROR, "Объект параметров отсутствует")
            return

        # Check whether method is incorrect
        if self.method not in available_methods:
            self.result = Error(METHOD_ERROR)
            return

    def get_response(self):
        response = {"id": self.request_id}

        if not self.result:
            self.result = merchant_api_methods.perform(self.method, self.params)

        response["error" if self.result.is_error() else "result"] = self.result.dict()

        return response
