from django.contrib import admin
from .models import LNMOnline, C2BPayment


class LNMOnlineAdmin(admin.ModelAdmin):
    list_display = ("PhoneNumber", "Amount", "MpesaReceiptNumber", "TransactionDate")

class C2BPaymentAdmin(admin.ModelAdmin):
    list_display = ("MSISDN", "TransAmount", "TransID", "TransTime")


admin.site.register(LNMOnline, LNMOnlineAdmin)
admin.site.register(C2BPayment, C2BPaymentAdmin)    