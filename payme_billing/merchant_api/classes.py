import abc

from payme_billing.vars.static import ERROR_MESSAGES

# Abstract class
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


# Wrapper for Error to raise an exception, containing the Error itself
class PaymeCheckFailedException(Exception):
    _error = None

    def __init__(self, code, additional_info=None):
        self._error = Error(code, additional_info)

    def error(self):
        return self._error