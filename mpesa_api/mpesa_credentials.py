import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64


class MpesaC2bCredential:
    consumer_key = 'xxxxxxx'
    consumer_secret = 'xxxxxx'
    test_msisdn = 254708374149
    #generating mpesa access token
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


# generate the access token
class MpesaAccessToken:
    r = requests.get(MpesaC2bCredential.api_URL,
                     auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']


#generating mpesa password as documented by saf
class LipanaMpesaPpassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S') #generating lipa na mpesa timestamp
    Business_short_code = "174379" #from mpesa sandbox test credentials
    Test_c2b_shortcode = "xxxxx"
    passkey = 'xxxxxxxxxxxxx'

    data_to_encode = Business_short_code + passkey + lipa_time

    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')
