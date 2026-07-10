import requests

from django.conf import settings



REQUEST_URL = (
    "https://api.zarinpal.com/pg/v4/payment/request.json"
)


VERIFY_URL = (
    "https://api.zarinpal.com/pg/v4/payment/verify.json"
)


START_PAY_URL = (
    "https://www.zarinpal.com/pg/StartPay/"
)





def request_payment(
    merchant_id,
    amount,
    callback_url,
    description
):


    data = {

        "merchant_id":
            merchant_id,

        "amount":
            amount,

        "description":
            description,

        "callback_url":
            callback_url
    }



    response = requests.post(
        REQUEST_URL,
        json=data
    )


    return response.json()







def verify_payment(
    merchant_id,
    amount,
    authority
):


    data = {

        "merchant_id":
            merchant_id,

        "amount":
            amount,

        "authority":
            authority
    }



    response = requests.post(
        VERIFY_URL,
        json=data
    )


    return response.json()







def get_payment_url(
    authority
):

    return (
        START_PAY_URL
        +
        authority
    )