# import json
# import Adyen
# import uuid
# import requests
# from flask import request, jsonify
# from main.config import get_adyen_api_key, get_adyen_merchant_account
# from helpers.random_string_helper import random_string
# from adyen_client import get_adyen_client


# # def adyen_payment_methods(selected_country):
# #     adyen = Adyen.Adyen()
# #     adyen.payment.client.xapikey = get_adyen_api_key()
# #     adyen.payment.client.platform = "test"
# #     adyen.payment.client.merchant_account = get_adyen_merchant_account()

# #     request_data = {
# #         "merchantAccount": get_adyen_merchant_account(),
# #         "countryCode": selected_country,
# #         "shopperReference": "TestShopperOne",
# #     }

# #     result = adyen.checkout.payments_api.payment_methods(request_data)
# #     return result.raw_response  # or json.loads(result.raw_response)


# def adyen_payment_methods():
#     print("adyen_payment_methods on app.py")
#     """
#     Calls the Adyen /paymentMethods endpoint.
#     Returns a list of available payment methods for the configured merchant account.
#     """

#     data = request.get_json()
#     selected_country = data.get("countryCode", "DE")
#     print("selected country fomr the backend", selected_country)

#     # Instantiate the Adyen client
#     adyen = get_adyen_client()

#     # adyen = Adyen.Adyen()
#     # adyen.payment.client.xapikey = get_adyen_api_key()
#     # adyen.payment.client.platform = "test"  # Use "live" in production
#     adyen.payment.client.merchant_account = get_adyen_merchant_account()

#     # Prepare the request payload
#     request_data = {
#         "merchantAccount": get_adyen_merchant_account(),
#         "countryCode": selected_country,
#         "shopperReference": "TestShopperOne",
#         # "allowedPaymentMethods": ["paypal", "blik"]
#     }

#     # Call the Adyen payments API's /paymentMethods endpoint
#     result = adyen.checkout.payments_api.payment_methods(request_data)
#     print("Result from adyen", result)

#     # Format the JSON response
#     formatted_response = json.dumps(json.loads(result.raw_response), indent=4)
#     print("/paymentMethods response:\n" + formatted_response)

#     return formatted_response


# def adyen_payments():
#     """
#     Calls the Adyen /payments endpoint.
#     Handles the initial payment request from the Drop-in or Components.
#     """
#     adyen = get_adyen_client()
#     # adyen = Adyen.Adyen()
#     # adyen.payment.client.xapikey = get_adyen_api_key()
#     # adyen.payment.client.platform = "test"
#     adyen.payment.client.merchant_account = get_adyen_merchant_account()

#     data = request.get_json()
#     print("!!!!!!data", data)
#     selected_currency = data.get("currency")
#     print("!!!!!! selected_currency", selected_currency)

#     payload = request.json
#     print("frontend payload", payload)

#     request_data = {
#         "merchantAccount": get_adyen_merchant_account(),
#         "reference": f"Reference {uuid.uuid4()}",
#         "amount": payload.get("amount", {"currency": selected_currency, "value": 1000}),
#         # "amount": payload.get("amount", {}),
#         #  "amount": {
#         #     "currency": "PLN",
#         #     "value": 1230
#         # },
#         "paymentMethod": payload.get("paymentMethod", {}),
#         "shopperLocale": "en_US",
#         "telephoneNumber": "+46 840 839 298",
#         "shopperEmail": "youremail@email.com",
#         "shopperName": {"firstName": "Testperson-se", "lastName": "Approved"},
#         # "redirectFromIssuerMethod": "GET",
#         # "redirectToIssuerMethod": "GET",
#         # "billingAddress": {
#         #     "city": "Ankeborg",
#         #     "country": "SE",
#         #     "houseNumberOrName": "1",
#         #     "postalCode": "12345",
#         #     "street": "Stargatan"
#         # },
#         # "deliveryAddress": {
#         #     "city": "Ankeborg",
#         #     "country": "SE",
#         #     "houseNumberOrName": "1",
#         #     "postalCode": "12345",
#         #     "street": "Stargatan"
#         # },
#         "returnUrl": "http://localhost:5000/result",
#         # PayPal config
#         "lineItems": [
#             {
#                 "quantity": "1",
#                 "description": "Red Shoes",
#                 "itemCategory": "PHYSICAL_GOODS",
#                 "sku": "ABC123",
#                 "amountExcludingTax": "500",
#                 "taxAmount": "10",
#             },
#             {
#                 "quantity": "1",
#                 "description": "Polkadot Socks",
#                 "itemCategory": "PHYSICAL_GOODS",
#                 "sku": "DEF234",
#                 "amountExcludingTax": "500",
#                 "taxAmount": "10",
#             },
#         ],
#         "additionalData": {"paypalRisk": "STATE_DATA"},
#         "shopperIP": "192.0.2.1",
#         #"shopperReference": "TestShopperOne",
#         # "shopperReference": random_string(),
#         "shopperInteraction": "Ecommerce",
#         "storePaymentMethod": True,
#         "recurringProcessingModel": "CardOnFile",
#         "channel": "web",
#         "shopperReference": "TestShopperOne",
#         "origin": "http://localhost:5000",
#         "browserInfo": {
#             "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
#             "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#             "language": "nl-NL",
#             "colorDepth": 24,
#             "screenHeight": 723,
#             "screenWidth": 1536,
#             "timeZoneOffset": 0,
#             "javaEnabled": True,
#         },
#     }

#     if payload.get("billingAddress"):
#         request_data["billingAddress"] = payload["billingAddress"]

#     # Also call /payments on payments_api:
#     print("request_data from payments call", request_data)
#     result = adyen.checkout.payments_api.payments(request_data)

#     # Parse the response
#     response_data = json.loads(result.raw_response)
#     formatted_response = json.dumps(response_data, indent=4)

#     print("/payments response:\n", formatted_response)

#     return formatted_response

# def payment_details():
#     details = request.get_json()
#     response = adyen.checkout.payments_api.payments_details(details)
#     return jsonify(response.message)

# def result_return():
#     redirect_result = request.args.get("redirectResult")

#     if not redirect_result:
#         return redirect(url_for("result_error"))

#     details_request = {
#         "details": {
#             "redirectResult": redirect_result
#         }
#     }

#     try:
#         response = adyen.checkout.payments_api.payments_details(details_request)
#         result_code = response.message.get("resultCode", "ERROR")
#         print("Adyen resultCode:", result_code)

#         if result_code == "Authorised":
#             return redirect(url_for("result_success"))
#         elif result_code in ["Pending", "Received"]:
#             return redirect(url_for("result_pending"))
#         elif result_code == "Refused":
#             return redirect(url_for("result_failed"))
#         else:
#             return redirect(url_for("result_error"))

#     except Exception as e:
#         print("Error during /result/return:", str(e))
#         return redirect(url_for("result_error"))


# # def hosted_checkout():

# # # Create the request object(s)
# # json_request = {
# #   "merchantAccount": "YOUR_MERCHANT_ACCOUNT",
# #   "amount": {
# #     "value": 1000,
# #     "currency": "EUR"
# #   },
# #   "returnUrl": "https://your-company.com/checkout?shopperOrder=12xy..",
# #   "reference": "YOUR_PAYMENT_REFERENCE",
# #   "mode": "hosted",
# #   "themeId": "AZ1234567",
# #   "countryCode": "NL",
# #   "expiresAt": "2023-05-18T10:15:30+01:00"
# # }

# # Send the request
# result = adyen.checkout.payments_api.sessions(request=json_request, idempotency_key="UUID")