from django.apps import apps
from django.db.models import Model

from bbu_academy.settings import PAYME_BILLING_SETTINGS

TEST = PAYME_BILLING_SETTINGS.get("test")
ADMIN = PAYME_BILLING_SETTINGS.get("admin")
WEB_CASH_ID = PAYME_BILLING_SETTINGS.get("test_web_cash_id") if TEST else PAYME_BILLING_SETTINGS.get("web_cash_id")
WEB_CASH_KEY = PAYME_BILLING_SETTINGS.get("test_web_cash_key") if TEST else PAYME_BILLING_SETTINGS.get("web_cash_key")
BILLING_MODEL = PAYME_BILLING_SETTINGS.get("billing_model")
_split = BILLING_MODEL.split(".")
MODEL: Model = apps.get_model(_split[0], _split[1])
