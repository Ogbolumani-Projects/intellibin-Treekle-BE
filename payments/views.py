from django.shortcuts import render, redirect
from .models import Payment, UserWallet, Subscription, PaymentRecord
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Subscription, PaymentRecord
from .serializers import SubscriptionSerializer, PaymentRecordSerializer
from .utils import initialize_payment, verify_payment

class SubscriptionView(APIView):
    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            subscription = serializer.save(user=request.user)
            return Response({'message': 'Subscription tier selected', 'tier': subscription.tier})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentInitializationView(APIView):
    def post(self, request):
        user = request.user
        amount = request.data.get('amount')
        email = user.email
        payment_response = initialize_payment(email, amount)
        if payment_response['status']:
            return Response({'authorization_url': payment_response['data']['authorization_url']})
        return Response({'error': 'Payment initialization failed'}, status=status.HTTP_400_BAD_REQUEST)

class PaymentVerificationView(APIView):
    def get(self, request, reference):
        verification_response = verify_payment(reference)
        if verification_response['status']:
            # Save the payment record
            PaymentRecord.objects.create(
                user=request.user,
                amount=verification_response['data']['amount'] / 100,
                reference=reference,
                status='success'
            )
            return Response({'message': 'Payment successful'})
        return Response({'error': 'Payment verification failed'}, status=status.HTTP_400_BAD_REQUEST)
