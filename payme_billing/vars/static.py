
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

AMOUNT_ERROR_MESSAGE = {"ru": "Неверная сумма", "uz": "not translated", "en": "The amount is incorrect"}
PHONE_ERROR_MESSAGE = {"ru": "Введённый номер телефона не найден", "uz": "not translated", "en": "Could not find phone number"}
RECEIPT_NOT_FOUND_ERROR_MESSAGE = {"ru": "Заказ не найден", "uz": "not translated", "en": "Could not find the order"}
RECEIPT_BUSY_ERROR_MESSAGE = {"ru": "Другая транзакция уже заняла этот заказ", "uz": "not translated", "en": "Another transaction has already booked requested order"}
RECEIPT_PAID_ERROR_MESSAGE = {"ru": "Заказ уже оплачен", "uz": "not translated", "en": "The order was already paid"}
RECEIPT_CANCELLED_ERROR_MESSAGE = {"ru": "Заказ был отменён", "uz": "not translated", "en": "The order was cancelled"}

ERROR_MESSAGES = {
    # Common errors
    REQUEST_METHOD_ERROR: {"message": {"ru": "Ошибка возникает в том случае, если метод запроса не POST"}},
    JSON_ERROR: {"message": {"ru": "Ошибка парсинга JSON"}},
    FIELD_ERROR: {"message": {"ru": "В RPC-запросе отсутствуют обязательные поля или тип полей не соответствует спецификации"}},
    METHOD_ERROR: {"message": {"ru": "Запрашиваемый метод не найден"}},  # В RPC-запросе имя запрашиваемого метода содержится в поле data.
    RIGHTS_ERROR: {"message": {"ru": "Недостаточно привилегий для выполнения метода"}},
    SYSTEM_ERROR: {"message": {"ru": "Системная (внутренняя ошибка)"}},  # Ошибку следует использовать в случае системных сбоев: отказа базы данных, отказа файловой системы и т.д.

    # CheckPerformTransaction errors
    AMOUNT_ERROR: {"message": AMOUNT_ERROR_MESSAGE},
    PHONE_ERROR: {"message": PHONE_ERROR_MESSAGE, "data": "account[phone]"},
    RECEIPT_NOT_FOUND_ERROR: {"message": RECEIPT_NOT_FOUND_ERROR_MESSAGE, "data": "account[purchase_id]"},
    RECEIPT_BUSY_ERROR: {"message": RECEIPT_BUSY_ERROR_MESSAGE, "data": "account[purchase_id]"},
    RECEIPT_PAID_ERROR: {"message": RECEIPT_PAID_ERROR_MESSAGE, "data": "account[purchase_id]"},
    RECEIPT_CANCELLED_ERROR: {"message": RECEIPT_CANCELLED_ERROR_MESSAGE, "data": "account[purchase_id]"},

    # CreateTransaction errors
    CANNOT_PERFORM_ERROR: {"message": {"ru": "Невозможно выполнить операцию."}},

    # PerformTransaction errors
    TRANSACTION_NOT_FOUND_ERROR: {"message": {"ru": "Транзакция не найдена"}},
}


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


available_methods = ("CheckPerformTransaction", "CreateTransaction", "PerformTransaction", "CancelTransaction", "CheckTransaction", "GetStatement")
