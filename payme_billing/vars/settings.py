from typing import List

from django.apps import apps
from django.db.models import Model

from bbu_academy.settings import PAYME_BILLING_SETTINGS

TEST = PAYME_BILLING_SETTINGS.get("test")
ADMIN = PAYME_BILLING_SETTINGS.get("admin")
WEB_CASH_ID = PAYME_BILLING_SETTINGS.get("web_cash_id")
WEB_CASH_KEY = PAYME_BILLING_SETTINGS.get("test_web_cash_key") if TEST else PAYME_BILLING_SETTINGS.get("web_cash_key")
BILLING_MODELS = PAYME_BILLING_SETTINGS.get("billing_models")
CALLBACK_TIME = PAYME_BILLING_SETTINGS.get("callback_time")
mapped_billing_models = map(lambda x: x.split("."), BILLING_MODELS)
MODELS: List[Model] = [apps.get_model(*item) for item in mapped_billing_models]

_URL = "https://checkout.paycom.uz/"
_TEST_URL = "https://test.paycom.uz/"
URL = _TEST_URL if TEST else _URL
