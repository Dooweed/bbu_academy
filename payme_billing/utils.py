import abc


# Abstract class
from typing import Tuple

from payme_billing.vars import ERROR_MESSAGES


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
        raise PaymeCheckFailedException(-32600, "Параметр amount не указан")
    elif not isinstance(amount, int):
        raise PaymeCheckFailedException(-32600, "Параметр amount имеет неверный тип")
    return amount

def check_account(params: dict) -> Tuple[int, str]:
    ACCOUNT_PHONE_LENGTH = 9

    account = params.get("account")
    if account is None:
        raise PaymeCheckFailedException(-32600, "Параметр account не указан")
    elif not isinstance(account, dict):
        raise PaymeCheckFailedException(-32600, "Параметр account имеет неверный тип")

    purchase_id = account.get("purchase_id")
    if purchase_id is None:
        raise PaymeCheckFailedException(-32600, "Параметр account[purchase_id] не указан")
    elif not isinstance(purchase_id, int):
        raise PaymeCheckFailedException(-32600, "Параметр account[purchase_id] имеет неверный тип")

    phone = account.get("phone")
    if phone is None:
        raise PaymeCheckFailedException(-32600, "Параметр account[phone] не указан")
    elif not phone.isdigit():
        raise PaymeCheckFailedException(-32600, "Параметр account[phone] не может быть конвертирован в число")
    elif not isinstance(phone, str):
        raise PaymeCheckFailedException(-32600, "Параметр account[phone] имеет неверный тип")
    elif len(phone) != ACCOUNT_PHONE_LENGTH:
        raise PaymeCheckFailedException(-32600, "Параметр account[phone] имеет неверную длину")

    return purchase_id, phone

def check_transaction_id(params: dict) -> str:
    TRANSACTION_ID_LENGTH = 24

    transaction_id = params.get("id")
    if transaction_id is None:
        raise PaymeCheckFailedException(-32600, "Параметр id не указан")
    elif not isinstance(transaction_id, str):
        raise PaymeCheckFailedException(-32600, "Параметр id имеет неверный тип")
    elif len(transaction_id) != TRANSACTION_ID_LENGTH:
        raise PaymeCheckFailedException(-32600, "Параметр id имеет неверную длину")

    return transaction_id
