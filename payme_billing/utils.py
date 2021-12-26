from base64 import b64encode

from payme_billing.vars.settings import URL, WEB_CASH_ID, CALLBACK_TIME, MODELS


def get_first_matching_model(id):
    for item in MODELS:
        queryset = item.objects.filter(id=id, payment_type="payme")
        if queryset.exists():
            return queryset

def get_payment_link(purchase_id, phone, amount, lang, return_url=None):
    params = f"m={WEB_CASH_ID};ac.purchase_id={purchase_id};ac.phone={phone};a={amount};l={lang};ct={CALLBACK_TIME}"
    if return_url:
        params += f";c={return_url}"
    params_bytes = b64encode(params.encode('utf-8'))
    return URL + params_bytes.decode()
