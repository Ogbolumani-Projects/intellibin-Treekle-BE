from django.urls import path
from .views import InitiatePaymentAPIView, VerifyPaymentAPIView

urlpatterns = [
    # ... other URLs ...
    path('payments/initiate/', InitiatePaymentAPIView.as_view(), name='initiate_payment'),
    path('payments/verify/<str:transaction_ref>/', VerifyPaymentAPIView.as_view(), name='verify_payment'),
]