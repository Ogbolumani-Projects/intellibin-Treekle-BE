from django.urls import path
from .paystack import *
from .views import SubscriptionView, PaymentInitializationView, PaymentVerificationView

urlpatterns = [
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('initialize/', PaymentInitializationView.as_view(), name='payment_initialize'),
    path('transaction/verify/<str:reference>/', PaymentVerificationView.as_view(), name='payment_verify'),
]

