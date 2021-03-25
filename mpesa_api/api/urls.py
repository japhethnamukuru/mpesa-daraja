from django.urls import path
from mpesa_api.api import views

urlpatterns = [
    path('lnm/', views.LNMCallbackApiView.as_view(), name = 'lnm_callback_url'),
    path('c2b-validation/', views.C2BValidationAPIView.as_view(), name = 'c2b_validation'),
    path('c2b-confirmation/', views.C2BConfirmationAPIView.as_view(), name = 'c2b_confirmation'),
]