from django.utils import translation

from bbu_academy.settings import LANGUAGES


def get_translation_in(language, string):
    with translation.override(language):
        return translation.gettext(string)


REQUEST_METHOD_ERROR = -32300
JSON_ERROR = -32700
FIELD_ERROR = -32600
METHOD_ERROR = -32601
RIGHTS_ERROR = -32504
SYSTEM_ERROR = -32400

AMOUNT_ERROR = -31001
PHONE_ERROR = -31051
RECEIPT_NOT_FOUND_ERROR = -31050
RECEIPT_BUSY_ERROR = -31060
RECEIPT_PAID_ERROR = -31061
RECEIPT_CANCELLED_ERROR = -31062

CANNOT_PERFORM_ERROR = -31008
TRANSACTION_NOT_FOUND_ERROR = -31003

# # # # # # # # # # # # # # Rewrite error codes as constants     <----
ERROR_MESSAGES = {
    # Common errors
    REQUEST_METHOD_ERROR: {"message": {"ru": "Ошибка возникает в том случае, если метод запроса не POST"}},
    JSON_ERROR: {"message": {"ru": "Ошибка парсинга JSON"}},
    FIELD_ERROR: {"message": {"ru": "В RPC-запросе отсутствуют обязательные поля или тип полей не соответствует спецификации"}},
    METHOD_ERROR: {"message": {"ru": "Запрашиваемый метод не найден"}},  # В RPC-запросе имя запрашиваемого метода содержится в поле data.
    RIGHTS_ERROR: {"message": {"ru": "Недостаточно привилегий для выполнения метода"}},
    SYSTEM_ERROR: {"message": {"ru": "Системная (внутренняя ошибка)"}},  # Ошибку следует использовать в случае системных сбоев: отказа базы данных, отказа файловой системы и т.д.

    # CheckPerformTransaction errors
    AMOUNT_ERROR: {"message": {lang[0]: get_translation_in(lang[0], "Неверная сумма") for lang in LANGUAGES}},
    PHONE_ERROR: {"message": {lang[0]: get_translation_in(lang[0], "Введённый номер телефона не найден") for lang in LANGUAGES}, "data": "account[phone]"},
    RECEIPT_NOT_FOUND_ERROR: {"message": {lang[0]: get_translation_in(lang[0], "Заказ не найден") for lang in LANGUAGES}, "data": "account[purchase_id]"},
    RECEIPT_BUSY_ERROR: {"message": {lang[0]: get_translation_in(lang[0], "Другая транзакция уже заняла этот заказ") for lang in LANGUAGES}, "data": "account[purchase_id]"},
    RECEIPT_PAID_ERROR: {"message": {lang[0]: get_translation_in(lang[0], "Заказ уже оплачен") for lang in LANGUAGES}, "data": "account[purchase_id]"},
    RECEIPT_CANCELLED_ERROR: {"message": {lang[0]: get_translation_in(lang[0], "Заказ был отменён") for lang in LANGUAGES}, "data": "account[purchase_id]"},

    # CreateTransaction errors
    CANNOT_PERFORM_ERROR: {"message": {"ru": "Невозможно выполнить операцию."}},

    # PerformTransaction errors
    TRANSACTION_NOT_FOUND_ERROR: {"message": {"ru": "Транзакция не найдена"}},
}
PAYME_RECEIPT_STATES = (
    (0, "Чек создан. Ожидание подтверждения оплаты."),
    (1, "Первая стадия проверок. Создание транзакции в биллинге мерчанта."),
    (2, "Списание денег с карты."),
    (3, "Закрытие транзакции в биллинге мерчанта."),
    (4, "Чек оплачен."),
    (20, "Чек стоит на паузе для ручного вмешательства."),
    (21, "Чек в очереди на отмену."),
    (30, "Чек в очереди на закрытие транзакции в биллинге мерчанта."),
    (50, "Чек отменен."),
)
PAYME_TRANSACTION_STATES = (
    (1, "Транзакция успешно создана, ожидание подтверждения (начальное состояние 0)"),
    (2, "Транзакция успешно завершена (начальное состояние 1)"),
    (-1, "Транзакция отменена (начальное состояние 1)"),
    (-2, "Транзакция отменена после завершения (начальное состояние 2)"),
)
PAYME_TRANSACTION_DENIAL_REASONS = (
    (1, "Один или несколько получателей не найдены или неактивны в Payme Business."),
    (2, "Ошибка при выполнении дебетовой операции в процессинговом центре."),
    (3, "Ошибка выполнения транзакции."),
    (4, "Транзакция отменена по таймауту."),
    (5, "Возврат денег."),
    (10, "Неизвестная ошибка."),
)
