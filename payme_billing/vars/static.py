# Common errors
REQUEST_METHOD_ERROR = -32300
JSON_ERROR = -32700
FIELD_ERROR = -32600
METHOD_ERROR = -32601
RIGHTS_ERROR = -32504
SYSTEM_ERROR = -32400

# CheckPerformTransaction errors
AMOUNT_ERROR = -31001
PHONE_ERROR = -31051
RECEIPT_NOT_FOUND_ERROR = -31050
RECEIPT_BUSY_ERROR = -31060
RECEIPT_PAID_ERROR = -31061
RECEIPT_CANCELLED_ERROR = -31062

# CreateTransaction errors
CANNOT_PERFORM_ERROR = -31008

# PerformTransaction errors
TRANSACTION_NOT_FOUND_ERROR = -31003

# CancelTransaction errors
CANNOT_CANCEL_ERROR = -31007


REQUEST_METHOD_ERROR_MESSAGE = {"ru": "Неверный метод запроса. Ожидается POST", "uz": "not translated", "en": "Incorrect request method. POST expected"}
JSON_ERROR_MESSAGE = {"ru": "Ошибка парсинга JSON", "uz": "not translated", "en": "JSON parse error"}
FIELD_ERROR_MESSAGE = {"ru": "В RPC-запросе отсутствуют обязательные поля или тип полей не соответствует спецификации", "uz": "not translated", "en": "RPC-request missing mandatory fields or field types does not match specification"}
METHOD_ERROR_MESSAGE = {"ru": "Запрашиваемый метод не найден", "uz": "not translated", "en": "Could not find requested method"}
RIGHTS_ERROR_MESSAGE = {"ru": "Недостаточно привилегий для выполнения метода", "uz": "not translated", "en": "Not enough rights to perform method"}
SYSTEM_ERROR_MESSAGE = {"ru": "Системная (внутренняя ошибка)", "uz": "not translated", "en": "System error (server error)"}

AMOUNT_ERROR_MESSAGE = {"ru": "Неверная сумма", "uz": "not translated", "en": "The amount is incorrect"}
PHONE_ERROR_MESSAGE = {"ru": "Введённый номер телефона не найден", "uz": "not translated", "en": "Could not find phone number"}
RECEIPT_NOT_FOUND_ERROR_MESSAGE = {"ru": "Заказ не найден", "uz": "not translated", "en": "Could not find the order"}
RECEIPT_BUSY_ERROR_MESSAGE = {"ru": "Другая транзакция уже заняла этот заказ", "uz": "not translated", "en": "Another transaction has already booked requested order"}
RECEIPT_PAID_ERROR_MESSAGE = {"ru": "Заказ уже оплачен", "uz": "not translated", "en": "The order was already paid"}
RECEIPT_CANCELLED_ERROR_MESSAGE = {"ru": "Заказ был отменён", "uz": "not translated", "en": "The order was cancelled"}

CANNOT_PERFORM_ERROR_MESSAGE = {"ru": "Невозможно выполнить операцию.", "uz": "not translated", "en": "Cannot perform the operation"}

TRANSACTION_NOT_FOUND_ERROR_MESSAGE = {"ru": "Транзакция не найдена", "uz": "not translated", "en": "Could not find the transaction"}

CANNOT_CANCEL_ERROR_MESSAGE = {"ru": "Заказ выполнен. Невозможно отменить транзакцию. Товар или услуга предоставлена покупателю в полном объеме.", "uz": "not translated", "en": "The order has been completed. Cannot cancel transaction. The product was fully provided to a customer"}

ERROR_MESSAGES = {
    REQUEST_METHOD_ERROR: {"message": REQUEST_METHOD_ERROR_MESSAGE},
    JSON_ERROR: {"message": JSON_ERROR_MESSAGE},
    FIELD_ERROR: {"message": FIELD_ERROR_MESSAGE},
    METHOD_ERROR: {"message": METHOD_ERROR_MESSAGE},  # В RPC-запросе имя запрашиваемого метода содержится в поле data.
    RIGHTS_ERROR: {"message": RIGHTS_ERROR_MESSAGE},
    SYSTEM_ERROR: {"message": SYSTEM_ERROR_MESSAGE},  # Ошибку следует использовать в случае системных сбоев: отказа базы данных, отказа файловой системы и т.д.

    AMOUNT_ERROR: {"message": AMOUNT_ERROR_MESSAGE},
    PHONE_ERROR: {"message": PHONE_ERROR_MESSAGE, "data": "account[phone]"},
    RECEIPT_NOT_FOUND_ERROR: {"message": RECEIPT_NOT_FOUND_ERROR_MESSAGE, "data": "account[purchase_id]"},
    RECEIPT_BUSY_ERROR: {"message": RECEIPT_BUSY_ERROR_MESSAGE, "data": "account[purchase_id]"},
    RECEIPT_PAID_ERROR: {"message": RECEIPT_PAID_ERROR_MESSAGE, "data": "account[purchase_id]"},
    RECEIPT_CANCELLED_ERROR: {"message": RECEIPT_CANCELLED_ERROR_MESSAGE, "data": "account[purchase_id]"},

    CANNOT_PERFORM_ERROR: {"message": CANNOT_PERFORM_ERROR_MESSAGE},

    TRANSACTION_NOT_FOUND_ERROR: {"message": TRANSACTION_NOT_FOUND_ERROR_MESSAGE},

    CANNOT_CANCEL_ERROR: {"message": CANNOT_CANCEL_ERROR_MESSAGE},
}


# Choices for PaymeTransaction "state" attribute
PAYME_TRANSACTION_STATES = (
    (1, "Транзакция успешно создана, ожидание подтверждения (начальное состояние 0)"),
    (2, "Транзакция успешно завершена (начальное состояние 1)"),
    (-1, "Транзакция отменена (начальное состояние 1)"),
    (-2, "Транзакция отменена после завершения (начальное состояние 2)"),
)


# Choices for PaymeTransaction "denial_reason" attribute
PAYME_TRANSACTION_DENIAL_REASONS = (
    (1, "Один или несколько получателей не найдены или неактивны в Payme Business."),
    (2, "Ошибка при выполнении дебетовой операции в процессинговом центре."),
    (3, "Ошибка выполнения транзакции."),
    (4, "Транзакция отменена по таймауту."),
    (5, "Возврат денег."),
    (10, "Неизвестная ошибка."),
)


# Choices for receipt "state" attribute
PAYME_RECEIPT_STATES = (
    #(None, '----'),
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

available_methods = ("CheckPerformTransaction", "CreateTransaction", "PerformTransaction", "CancelTransaction", "CheckTransaction", "GetStatement")
