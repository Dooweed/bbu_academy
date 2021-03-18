from base64 import b64encode

from payme_billing.vars.settings import URL, WEB_CASH_ID


def get_payment_link(purchase_id, phone, amount, lang, return_url=None):
    params = f"m={WEB_CASH_ID};ac.purchase_id={purchase_id};ac.phone={phone};amount={amount};lang={lang}"
    if return_url:
        params += f"c={return_url}"
    url = f"{URL}/{b64encode(params.encode())}"
    return url
