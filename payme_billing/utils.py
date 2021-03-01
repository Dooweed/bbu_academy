import abc


# Abstract class
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

    def __init__(self, code):
        if code not in ERROR_MESSAGES:
            raise ValueError(f"Код ошибки {code} не существует")
        else:
            self.code = code

    def __dict__(self):
        error_obj = {"code": self.code}

        message = ERROR_MESSAGES[self.code].get("message")
        if message:
            error_obj["message"] = message

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
