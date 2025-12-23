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
    (print(f"[paymentMethod] payload{payload['paymentMethod']}"),)

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
        # "shopperInteraction": "Moto",
        "allowedPaymentMethods": ["scheme"],
        # "storePaymentMethod": True,
        "recurringProcessingModel": "CardOnFile",
        "origin": "http://localhost:5000",
        # "captureDelayHours": 2

        # Paypal specific payload
        "lineItems": [
            {
                "amountIncludingTax": 5995,
                "description": "Style PETE",
                "id": "204500_70418600_23_XXL",
                "quantity": 1,
                "sku": "204500_70418600_23_XXL",
            }
        ],

        # Klarna specific payload
        "telephoneNumber": "+46 840 839 298",
        "shopperEmail": "valeria.furin@adyen.com",
        "shopperName": {"firstName": "Testperson-se", "lastName": "Approved"},
        # "billingAddress": {
        #     "city": "Ankeborg",
        #     "country": "SE",
        #     "houseNumberOrName": "1",
        #     "postalCode": "12345",
        #     "street": "Stargatan",
        # },
        # "deliveryAddress": {
        #     "city": "Ankeborg",
        #     "country": "SE",
        #     "houseNumberOrName": "1",
        #     "postalCode": "12345",
        #     "street": "Stargatan",
        # },
        # "metadata": {
        #     "test": "test"
        # },
        # "lineItems": [
        #     {
        #         "quantity": "1",
        #         "taxPercentage": "2100",
        #         "description": "Shoes",
        #         "id": "Item #1",
        #         "amountIncludingTax": "400",
        #         "productUrl": "URL_TO_PURCHASED_ITEM",
        #         "imageUrl": "URL_TO_PICTURE_OF_PURCHASED_ITEM",
        #     },
        #     {
        #         "quantity": "2",
        #         "taxPercentage": "2100",
        #         "description": "Socks",
        #         "id": "Item #2",
        #         "amountIncludingTax": "300",
        #         "productUrl": "URL_TO_PURCHASED_ITEM",
        #         "imageUrl": "URL_TO_PICTURE_OF_PURCHASED_ITEM",
        #     },
        # ],

        # Ratepay
        # "dateOfBirth": "1970-07-10",
        # "bankAccount": {
        #     "countryCode": "DE",
        #     "iban": "DE87123456781234567890",
        #     "ownerName": "A. Schneider",
        # },
        # "deviceFingerprint": "1b9d6bcdbbfd4b2d9b5dab8dfbbd4bed",

        # Riverty
        # "lineItems": [
        #   {
        #       "quantity": "1",
        #       "taxPercentage": "2000",
        #       "description": "Polo shirt",
        #       "id": "Item #1",
        #       "itemCategory": "Shirts",
        #       "amountIncludingTax": "1200",
        #       "taxAmount": "200",
        #       "amountExcludingTax": "1000",
        #       "productUrl": "https://www.mystoredemo.io#/product/01",
        #       "imageUrl": "https://www.mystoredemo.io/1689f3f40b292d1de2c6.png"
        #   },
        # ],
        # "billingAddress": {
        #     "city": "Berlin",
        #     "country": "DE",
        #     "houseNumberOrName": "1",
        #     "postalCode": "12345",
        #     "street": "Test",
        # },
        # "shopperIP": "123.123.123.123",
    }

    if payload.get("billingAddress"):
        request_data["billingAddress"] = payload["billingAddress"]

    print(f"[make_payment] Request data: {request_data}")

    response = adyen.checkout.payments_api.payments(request_data).message

    print(f"response", response)
    return response


def handle_payment_details(details_payload):
    adyen = get_adyen_client()
    payment_detail_response = adyen.checkout.payments_api.payments_details(details_payload).message

    return payment_detail_response


def create_adyen_session():
    adyen = get_adyen_client()
    request_data = {
        "merchantAccount": ADYEN_MERCHANT_ACCOUNT,
        "channel": "Web",
        "reference": f"Reference-{uuid.uuid4()}",
        "countryCode": "DE",
        "shopperLocale": "en-US",
        "amount": {
            "currency": "EUR",
            "value": "10000"
        },
        "returnUrl": "http://localhost:5000/result/return",
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

    print(f"[sessions] Request data: {request_data}")

    response = adyen.checkout.payments_api.sessions(request_data).message

    print("response", response)
    return response
