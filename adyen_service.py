from adyen_client import get_adyen_client
import os
import uuid

ADYEN_MERCHANT_ACCOUNT = os.getenv("ADYEN_MERCHANT_ACCOUNT")

def get_payment_methods(country_code="DE"):
    adyen = get_adyen_client()
    request_data = {
        "merchantAccount": ADYEN_MERCHANT_ACCOUNT,
        "channel": "Web",
        "countryCode": country_code,
        "shopperLocale": "en-US",
    }

    return adyen.checkout.payments_api.payment_methods(request=request_data).message


def make_payment(payload):
    adyen = get_adyen_client()

    # print(f"[make_payment] payload{payload}"),
    print(f"[paymentMethod] payload{payload['paymentMethod']}"),

    request_data = {
        # "amount": payload.get("amount", {"currency": payload.get("currency"), "value": 1010}),
        "amount": payload.get("amount"),
        "reference": f"Reference-{uuid.uuid4()}",
        "paymentMethod": payload.get("paymentMethod"),
        "returnUrl": "http://localhost:5000/result/return",
        "merchantAccount": ADYEN_MERCHANT_ACCOUNT,
        "channel": "Web",
        "countryCode": payload.get("countryCode"),
        "browserInfo": payload.get("browserInfo", {}),
        "shopperReference": "TestShopperOneTwoTwo",
        "shopperInteraction": "Ecommerce",
        "storePaymentMethod": True,
        "recurringProcessingModel": "CardOnFile",
        "origin": "http://localhost:5000",
        # "captureDelayHours": 2

        # Klarna specific payload
        "telephoneNumber": "+46 840 839 298",
        "shopperEmail": "youremail@email.com",
        "shopperName": {"firstName": "Testperson-se", "lastName": "Approved"},
        "billingAddress": {
            "city": "Ankeborg",
            "country": "SE",
            "houseNumberOrName": "1",
            "postalCode": "12345",
            "street": "Stargatan",
        },
        "deliveryAddress": {
            "city": "Ankeborg",
            "country": "SE",
            "houseNumberOrName": "1",
            "postalCode": "12345",
            "street": "Stargatan",
        },
        "lineItems": [
            {
                "quantity": "1",
                "taxPercentage": "2100",
                "description": "Shoes",
                "id": "Item #1",
                "amountIncludingTax": "400",
                "productUrl": "URL_TO_PURCHASED_ITEM",
                "imageUrl": "URL_TO_PICTURE_OF_PURCHASED_ITEM",
            },
            {
                "quantity": "2",
                "taxPercentage": "2100",
                "description": "Socks",
                "id": "Item #2",
                "amountIncludingTax": "300",
                "productUrl": "URL_TO_PURCHASED_ITEM",
                "imageUrl": "URL_TO_PICTURE_OF_PURCHASED_ITEM",
            },
        ],
    }

    if payload.get("billingAddress"):
        request_data["billingAddress"] = payload["billingAddress"]

    print(f"[make_payment] Request data: {request_data}")

    response = adyen.checkout.payments_api.payments(request_data).message

    print("response", response)
    return response


def handle_payment_details(details_payload):
    adyen = get_adyen_client()
    return adyen.checkout.payments_api.payments_details(details_payload).message
