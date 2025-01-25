from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PaymentSerializer
from paystackapi.transaction import Transaction

class InitiatePaymentAPIView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            user = serializer.validated_data['user']
            # Create a Paystack transaction
            transaction = Transaction.initialize(
                amount=int(amount * 100),  # Paystack requires amount in kobo (cents)
                email=user.email,
                # Add other Paystack parameters as needed (e.g., reference, callback_url)
            )
            return Response(transaction, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyPaymentAPIView(APIView):
    def get(self, request, transaction_ref):
        try:
            # Verify the transaction with Paystack
            transaction = Transaction.verify(transaction_ref)
            # Update payment status in your database
            payment = Payment.objects.get(transaction_ref=transaction_ref)
            payment.status = 'success'  # Or another appropriate status
            payment.save()
            return Response(transaction, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)