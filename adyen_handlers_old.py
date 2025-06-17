# # adyen_handlers.py

# import os
# from flask import jsonify, request, redirect, url_for
# import Adyen
# from adyen_client import get_adyen_client
# from dotenv import load_dotenv

# load_dotenv()

# # Initialize Adyen client
# adyen = get_adyen_client()

# # adyen = Adyen.Adyen()
# # adyen.client.xapikey = os.getenv('ADYEN_API_KEY')
# # adyen.client.platform = os.getenv('ADYEN_ENVIRONMENT', 'test')

# # def payment_methods():
# #     data = request.get_json()
# #     selected_country = data.get("countryCode", "DE")

# #     print("Selected country:", selected_country)

# #     try:
# #         result = adyen_payment_methods(selected_country)
# #         return jsonify(result)
# #     except Exception as e:
# #         print("Error getting payment methods:", e)
# #         return jsonify({"error": "Failed to retrieve payment methods"}), 500


# def payment_methods():
#     data = request.get_json()
#     selected_country = data.get("countryCode", "DE")

#     json_request = {
#         "merchantAccount": "TestCompany_ValeriaFurinUC_TEST",
#         "countryCode": selected_country,
#         "channel": "Web",
#         "shopperLocale": "en-US"
#     }

#     result = adyen.checkout.payments_api.payment_methods(request=json_request)
#     print("server payment methods response", result)
#     return jsonify(result.message)


# def payments():
#     payment_info = request.get_json()

#     request_info = {
#         'amount': {
#             'currency': 'EUR',
#             'value': 12300
#         },
#         'reference': 'YOUR_ORDER_REFERENCE',
#         'paymentMethod': payment_info['paymentMethod'],
#         'returnUrl': 'http://localhost:5000/result/return',
#         'merchantAccount': os.getenv('ADYEN_MERCHANT_ACCOUNT'),
#         'channel': 'Web',
#         'browserInfo': {
#             'userAgent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9) Gecko/2008052912 Firefox/3.0',
#             'acceptHeader': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#             'javaEnabled': True,
#             'colorDepth': 10,
#             'screenHeight': 2000,
#             'screenWidth': 3000,
#             'timeZoneOffset': 5,
#             'language': 'en'
#         },
#     }

#     response = adyen.checkout.payments_api.payments(request_info)
#     print("/Payments result ", response)
#     return jsonify(response.message)


# def payment_details():
#     details = request.get_json()
#     response = adyen.checkout.payments_api.payments_details(details)
#     print("response from details", response.message)
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
#         print("response from details in resukt return function", response.message)
#         result_code = response.message.get("resultCode", "ERROR")
#         print("Adyen resultCode:", result_code)

#         if result_code == "Authorised":
#             return redirect(url_for("success"))
#         elif result_code in ["Pending", "Received"]:
#             return redirect(url_for("pending"))
#         elif result_code == "Refused":
#             return redirect(url_for("failed"))
#         else:
#             return redirect(url_for("error"))

#     except Exception as e:
#         print("Error during /result/return:", str(e))
#         return redirect(url_for("error"))
