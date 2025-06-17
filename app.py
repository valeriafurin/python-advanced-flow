from flask import Flask, render_template, request, redirect, jsonify
from adyen_handlers import payment_methods, payments, payment_details, result_return
from main.config import *
from urllib.parse import unquote
import logging
import base64
import json
import os
from dotenv import load_dotenv

load_dotenv()

def page_not_found(error):
    return render_template('error.html'), 404

def create_app():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    app = Flask('app')
    app.secret_key = get_secret_session_key()

    app.register_error_handler(404, page_not_found)

    @app.route('/api/save-selection', methods=['POST'])
    def save_selection():
        data = request.get_json()
        print("this is the data from save-selection", data)

        if not data or 'country' not in data:
            return {"error": "No country selected"}, 400

        selected_country = data['country']
        selected_currency = data.get('currency')

        print(f"Received country selection: {selected_country}, currency: {selected_currency}")

        return {"message": f"Saved {selected_country} with {selected_currency} currency"}

    @app.route('/')
    def index():
        return render_template('index.html', client_key=get_adyen_client_key())

    @app.route('/success')
    def success():
        return render_template('success.html')

    @app.route('/failed')
    def failed():
        return render_template('failure.html')

    @app.route('/pending')
    def pending():
        return render_template('pending.html')

    @app.route('/error')
    def error():
        return render_template('error.html')

    @app.route('/dropin')
    def dropin():
        return render_template('dropin.html', client_key=get_adyen_client_key())

    @app.route('/components')
    def components():
        return render_template('components.html', client_key=get_adyen_client_key())

    @app.route('/api-only')
    def apiOnly():
        return render_template('api-only.html', client_key=get_adyen_client_key())

    @app.route('/api/paymentMethods', methods=['POST'])
    def payment_methods_route():
        return payment_methods()

    @app.route('/api/payments', methods=['POST'])
    def payments_route():
        return payments()


    @app.route('/api/payments/details', methods=['POST'])
    def payments_details_route():
        return payment_details()


    @app.route('/result/return')
    def result_return_route():
        return result_return()

    @app.route('/handleShopperRedirect', methods=['GET', 'POST'])
    def handle_shopper_redirect():
        try:
            redirect_result = request.args.get('redirectResult') if request.method == 'GET' else request.json.get('redirectResult')
            payload = request.args.get('payload') if request.method == 'GET' else request.json.get('payload')

            details = {}

            if redirect_result:
                details['redirectResult'] = redirect_result
            elif payload:
                details['payload'] = payload

            response = adyen_client.checkout.payments_api.payments_details(request={"details": details})

            result_code = response['resultCode']

            if result_code == "Authorised":
                return render_template('success.html') 
            elif result_code in ["Pending", "Received"]:
                return render_template('pending.html') 
            elif result_code == "Refused":
                return render_template('refused.html') 
            else:
                return render_template('error.html') 
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            return render_template('error.html') 

    return app

if __name__ == '__main__':
    web_app = create_app()

    logging.info(f"Running on http://localhost:{get_port()}")
    web_app.run(debug=True, port=get_port(), host='0.0.0.0')
