from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from mpesa_api.api.serializers import LNMOnlineSerializer, C2BPaymentSerializer
from mpesa_api.models import LNMOnline, C2BPayment

from datetime import datetime

import pytz


class LNMCallbackApiView(CreateAPIView):
    queryset = LNMOnline.objects.all()
    serializer_class = LNMOnlineSerializer
    permission_classes = [AllowAny]


    def create(self, request):
        print(request.data, "this is request.data")


        """
        safaricom response sample
        {
            'Body': 
            {
                'stkCallback': 
                {
                    'MerchantRequestID': '25388-24421343-1', 
                    'CheckoutRequestID': 'ws_CO_120320211408374962', 
                    'ResultCode': 0, 
                    'ResultDesc': 'The service request is processed successfully.', 
                    'CallbackMetadata': 
                    {
                        'Item': 
                        [
                            {
                                'Name': 'Amount', 
                                'Value': 1.0
                            }, 
                            {
                                'Name': 'MpesaReceiptNumber', 
                                'Value': 'PCC4LMYMEQ'
                            }, 
                            {
                                'Name': 'Balance'
                            }, 
                            {
                                'Name': 'TransactionDate', 
                                'Value': 20210312140848
                            }, 
                            {
                                'Name': 'PhoneNumber', 
                                'Value': 254795002433
                            }
                        ]
                    }
                }
            }
        } 
        this is request.data    
        """

        merchant_request_id = request.data["Body"]["stkCallback"]["MerchantRequestID"]
        print(merchant_request_id, "This should be MerchantRequestId")

        checkout_request_id = request.data["Body"]["stkCallback"]["CheckoutRequestID"]
        result_code = request.data["Body"]["stkCallback"]["ResultCode"]
        result_description = request.data["Body"]["stkCallback"]["ResultDesc"]

        amount = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
        print(amount, "this should be amount")

        mpesa_receipt_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
        print(mpesa_receipt_number, "This should be mpesa receipt number")

        balance = ""

        transaction_date = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"]
        print(transaction_date, "this should be transaction date")

        phone_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]
        print(phone_number, "Thid should be phone number")


        #converting string formatted date back to normal date
        str_transacton_date = str(transaction_date)
        print(str_transacton_date, "this is string transaction date")

        transaction_datetime = datetime.strptime(str_transacton_date, "%Y%m%d%H%M%S")
        print(transaction_datetime, "this should be transaction datetime")

        
        aware_transaction_datetime = pytz.utc.localize(transaction_datetime)
        print(aware_transaction_datetime, "this is aware transaction datetime")

        #create the model with the extracted values
        mpesa_model = LNMOnline.objects.create(
            CheckoutRequestId = checkout_request_id,
            MerchantRequestID = merchant_request_id,
            ResultDec = result_description,
            ResultCode = result_code,
            Amount = amount,
            MpesaReceiptNumber = mpesa_receipt_number,
            Balance = balance,
            TransactionDate = aware_transaction_datetime,
            PhoneNumber = phone_number
        )

        #saving the model
        mpesa_model.save()


        return Response({"WorkingResult": "Yeey!! it worked"})


class C2BValidationAPIView(CreateAPIView):
    queryset = C2BPayment.objects.all()
    serializer_class = C2BPaymentSerializer
    permission_classes = [AllowAny]


    # def create(self, request):
    #     print(request.data, "this is request.data in validation")

    #       return Response({"WorkingResult": "Yeey!! it worked"})


class C2BConfirmationAPIView(CreateAPIView):
    queryset = C2BPayment.objects.all()
    serializer_class = C2BPaymentSerializer
    permission_classes = [AllowAny]


    # def create(self, request):
    #     print(request.data, "this is request.data in confirmation")

    #     return Response({"ResultDesc": 0})


    #     """
    #     safaricom confirmation response sample
    #      {
    #          'TransactionType': 'Pay Bill', 
    #          'TransID': 'PCN01HIO7I', 
    #          'TransTime': '20210323201234', 
    #          'TransAmount': '1.00', 
    #          'BusinessShortCode': '603021', 
    #          'BillRefNumber': 'Namukuru', 
    #          'InvoiceNumber': '', 
    #          'OrgAccountBalance': '8647246.13', 
    #          'ThirdPartyTransID': '', 
    #          'MSISDN': '254708374149', 
    #          'FirstName': 'John', 
    #          'MiddleName': 'J.', 
    #          'LastName': 'Doe'
    #     } 
    #     this is request.data in confirmation
    #     """          

        