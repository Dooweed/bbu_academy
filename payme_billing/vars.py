from django.apps import apps
from django.db.models import Model
from django.utils import translation

from bbu_academy.settings import PAYME_BILLING_SETTINGS, LANGUAGES

TEST = PAYME_BILLING_SETTINGS.get("test")

WEB_CASH_ID = PAYME_BILLING_SETTINGS.get("test_web_cash_id") if TEST else PAYME_BILLING_SETTINGS.get("web_cash_id")

WEB_CASH_KEY = PAYME_BILLING_SETTINGS.get("test_web_cash_key") if TEST else PAYME_BILLING_SETTINGS.get("web_cash_key")

BILLING_MODEL = PAYME_BILLING_SETTINGS.get("billing_model")

_split = BILLING_MODEL.split(".")
MODEL: Model = apps.get_model(_split[0], _split[1], True)


def get_translation_in(language, string):
    with translation.override(language):
        return translation.gettext(string)


ERROR_MESSAGES = {
    # Common errors
    -32300: {"message": {"ru": "Ошибка возникает в том случае, если метод запроса не POST"}},
    -32700: {"message": {"ru": "Ошибка парсинга JSON"}},
    -32600: {"message": {"ru": "В RPC-запросе отсутствуют обязательные поля или тип полей не соответствует спецификации"}},
    -32601: {"message": {"ru": "Запрашиваемый метод не найден"}},  # В RPC-запросе имя запрашиваемого метода содержится в поле data.
    -32504: {"message": {"ru": "Недостаточно привилегий для выполнения метода"}},
    -32400: {"message": {"ru": "Системная (внутренняя ошибка)"}},  # Ошибку следует использовать в случае системных сбоев: отказа базы данных, отказа файловой системы и т.д.

    # CheckPerformTransaction errors
    -31001: {"message": {lang[0]: get_translation_in(lang[0], "Неверная сумма") for lang in LANGUAGES}},
    -31050: {"message": {lang[0]: get_translation_in(lang[0], "Заказ не найден") for lang in LANGUAGES}, "data": "account[purchase_id]"},
    -31051: {"message": {lang[0]: get_translation_in(lang[0], "Введённый номер телефона не найден") for lang in LANGUAGES}, "data": "account[phone]"},

    # CreateTransaction errors
    -31008: {"message": {"ru": "Невозможно выполнить операцию."}},

    # PerformTransaction errors
    -31003: {"message": {"ru": "Транзакция не найдена"}},
}
