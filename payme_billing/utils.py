import abc


# Abstract class
from typing import Tuple

from payme_billing.vars.static import FIELD_ERROR, ERROR_MESSAGES


class PaymeResponse:
    @abc.abstractmethod
    def __dict__(self) -> dict:
        pass

    @abc.abstractmethod
    def is_error(self) -> bool:
        pass

    def dict(self):
        return self.__dict__()

# Concrete class
class Error(PaymeResponse):
    code = None
    additional_info = None

    def __init__(self, code, additional_info=None):
        self.additional_info = additional_info
        if code not in ERROR_MESSAGES:
            raise ValueError(f"Код ошибки {code} не существует")
        else:
            self.code = code

    def __dict__(self):
        error_obj = {"code": self.code}

        message = ERROR_MESSAGES[self.code].get("message")
        if message:
            error_obj["message"] = message
            if self.additional_info:
                error_obj["additional_info"] = self.additional_info

        data = ERROR_MESSAGES[self.code].get("data")
        if data:
            error_obj["data"] = data

        return error_obj

    def is_error(self) -> bool:
        return True

# Concrete class
class Correct(PaymeResponse):
    response = None

    def __init__(self, response):
        self.response = response

    def __dict__(self):
        return self.response

    def is_error(self) -> bool:
        return False

# Exception container for Error
class PaymeCheckFailedException(Exception):
    _error = None

    def __init__(self, code, additional_info=None):
        self._error = Error(code, additional_info)

    def error(self):
        return self._error


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
    elif not purchase_id.isdigit():
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр account[purchase_id] не может быть конвертирован в число")

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

def check_time(params: dict) -> int:
    time = params.get("time")

    if time is None:
        raise PaymeCheckFailedException(FIELD_ERROR, "Время создания транзакции не указано")
    elif not isinstance(time, int):
        raise PaymeCheckFailedException(FIELD_ERROR, "Параметр time имеет неверный тип")

    return int(time/1000)

def check_time_diapason(params: dict) -> Tuple[int, int]:
    time_from, time_to = params.get("from"), params.get("to")

    if time_from is None:
        raise PaymeCheckFailedException(FIELD_ERROR, "Левая граница времени (from) не указана")
    elif time_to is None:
        raise PaymeCheckFailedException(FIELD_ERROR, "Левая граница времени (to) не указана")
    elif not isinstance(time_from, int):
        raise PaymeCheckFailedException(FIELD_ERROR, "Левая граница времени (from) имеет неверный тип")
    elif not isinstance(time_to, int):
        raise PaymeCheckFailedException(FIELD_ERROR, "Левая граница времени (to) имеет неверный тип")

    return int(time_from/1000), int(time_to/1000)
