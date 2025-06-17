import Adyen
import os
from dotenv import load_dotenv

load_dotenv()

def get_adyen_client():
    adyen = Adyen.Adyen()
    adyen.client.xapikey = os.getenv('ADYEN_API_KEY')
    adyen.client.platform = os.getenv('ADYEN_ENVIRONMENT', 'test')
    return adyen
