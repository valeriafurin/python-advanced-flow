from adyen_client import get_adyen_client
import os
import uuid

ADYEN_MERCHANT_ACCOUNT = os.getenv("ADYEN_MERCHANT_ACCOUNT")

def get_payment_methods(country_code="DE"):
    adyen = get_adyen_client()
    request_data = {
        "merchantAccount": ADYEN_MERCHANT_ACCOUNT,
        "countryCode": country_code,
        "channel": "Web",
        "shopperLocale": "en-US"
    }
    return adyen.checkout.payments_api.payment_methods(request=request_data).message

def make_payment(payload):
    adyen = get_adyen_client()

    request_data = {
        "amount": payload.get("amount", {"currency": "EUR", "value": 1000}),
        "reference": f"Reference-{uuid.uuid4()}",
        "paymentMethod": payload["paymentMethod"],
        "returnUrl": "http://localhost:5000/result/return",
        "merchantAccount": ADYEN_MERCHANT_ACCOUNT,
        "channel": "Web",
        "browserInfo": payload.get("browserInfo", {}),
        "shopperReference": "TestShopperOne",
        "shopperInteraction": "Ecommerce",
        "storePaymentMethod": True,
        "recurringProcessingModel": "CardOnFile",
        "origin": "http://localhost:5000"
    }

    if payload.get("billingAddress"):
        request_data["billingAddress"] = payload["billingAddress"]

    return adyen.checkout.payments_api.payments(request_data).message

def handle_payment_details(details_payload):
    adyen = get_adyen_client()
    return adyen.checkout.payments_api.payments_details(details_payload).message
