import requests


ZARINPAL_REQUEST_URL = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZARINPAL_VERIFY_URL = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZARINPAL_STARTPAY_URL = "https://www.zarinpal.com/pg/StartPay/"


def request_payment(merchant_id, amount, callback_url, description):

    payload = {
        "merchant_id": merchant_id,
        "amount": amount,
        "callback_url": callback_url,
        "description": description,
    }

    response = requests.post(
        ZARINPAL_REQUEST_URL,
        json=payload,
        timeout=10
    )

    return response.json()


def verify_payment(merchant_id, amount, authority):

    payload = {
        "merchant_id": merchant_id,
        "amount": amount,
        "authority": authority,
    }

    response = requests.post(
        ZARINPAL_VERIFY_URL,
        json=payload,
        timeout=10
    )

    return response.json()


def get_payment_url(authority):

    return f"{ZARINPAL_STARTPAY_URL}{authority}"