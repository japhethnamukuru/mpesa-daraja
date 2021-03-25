from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
#python library for making http request
import requests 
from requests.auth import HTTPBasicAuth
import json #for pssing json string using json.loads() 
from .mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword, MpesaC2bCredential
#allow MpesaCalls to post data in our applications.
from django.views.decorators.csrf import csrf_exempt 


#the stk push method
def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254717766906,  
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254717766906, 
        "CallBackURL": "https://intense-fortress-97977.herokuapp.com/api/payments/lnm/", # confirmation url
        "AccountReference": "Namukuru",
        "TransactionDesc": "Testing stk push"
    }

    #nitiate a post request to mpesa api bypassing the URL, the option variable and passing the headers.
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success') 


#register confirmation and validation URL with Safaricom.
@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token #generate mpesa access token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl" #register urls
    headers = {"Authorization": "Bearer %s" % access_token}

    #passing our Shortcode, ResponseType, ConfirmationUrl, and ValidationUrl.
    options = {"ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://intense-fortress-97977.herokuapp.com/api/payments/c2b-confirmation/",
               "ValidationURL": "https://intense-fortress-97977.herokuapp.com/api/payments/c2b-validation/"}
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)


# simulate the manual c2b transaction   
def simulate_transaction(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    headers = {"Authorization":"Bearer %s" % access_token}
    request = { 
    "ShortCode":LipanaMpesaPpassword.Test_c2b_shortcode,
    "CommandID":"CustomerPayBillOnline",
    "Amount":1,
    "Msisdn":MpesaC2bCredential.test_msisdn,
    "BillRefNumber":"Namukuru" 
    }
  
    response = requests.post(api_url, json = request, headers=headers)
    return HttpResponse('success')
