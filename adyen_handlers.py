from flask import jsonify, request, redirect, url_for
from adyen_service import get_payment_methods, make_payment, handle_payment_details, create_adyen_session


def payment_methods():
    data = request.get_json()
    selected_country = data.get("countryCode", "DE")

    try:
        result = get_payment_methods(selected_country)
        return jsonify(result)
    except Exception as e:
        print("Error getting payment methods:", e)
        return jsonify({"error": "Failed to retrieve payment methods"}), 500


def payments():
    payload = request.get_json()
    try:
        result = make_payment(payload)
        return jsonify(result)
    except Exception as e:
        print("Error processing payment:", e)
        return jsonify({"error": "Payment processing failed"}), 500


def payment_details():
    details = request.get_json()
    try:
        result = handle_payment_details(details)
        return jsonify(result)
    except Exception as e:
        print("Error retrieving payment details:", e)
        return jsonify({"error": "Failed to retrieve payment details"}), 500

def adyen_sessions():
    payload = request.get_json()
    try:            
        result = create_adyen_session()
        return jsonify(result)
    except Exception as e:
        print("Error creating Adyen session:", e)
        return jsonify({"error": "Failed to create Adyen session"}), 500


def result_return():
    redirect_result = request.args.get("redirectResult")

    if not redirect_result:
        return redirect(url_for("result_error"))

    details_request = {
        "details": {
            "redirectResult": redirect_result
        }
    }

    try:
        result = handle_payment_details(details_request)
        print(f"!!!!payment_detail_response", result)
        
        result_code = result.get("resultCode", "ERROR")

        if result_code == "Authorised":
            return redirect(url_for("success"))
        elif result_code in ["Pending", "Received"]:
            return redirect(url_for("pending"))
        elif result_code == "Refused":
            return redirect(url_for("failed"))
        else:
            return redirect(url_for("error"))

    except Exception as e:
        print("Error during /result/return:", str(e))
        return redirect(url_for("error"))
