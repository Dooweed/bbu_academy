from base64 import b64encode

from payme_billing.vars.settings import URL, WEB_CASH_ID


def get_payment_link(purchase_id, phone, amount, lang):
    params = f"m={WEB_CASH_ID};ac.purchase_id={purchase_id};ac.phone={phone};amount={amount};lang={lang}"
    url = f"{URL}/{b64encode(params.encode())}"
    return url
