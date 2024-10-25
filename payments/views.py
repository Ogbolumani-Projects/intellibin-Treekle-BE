from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Subscription, PaymentRecord
from .serializers import SubscriptionSerializer, PaymentRecordSerializer
from .utils import initialize_payment, verify_payment
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from authservice.models import CustomUser
from datetime import datetime, timedelta, timezone
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class SubscriptionView(APIView):
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            user = CustomUser.objects.get(id= user_id)
            one_month_from_now = datetime.now(timezone.utc) + timedelta(days=30)
            subscription = serializer.save(user=user, end_date=one_month_from_now)
            return Response({'message': 'Subscription tier selected', 'tier': subscription.tier})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentInitializationView(APIView):
    def post(self, request):
        user = request.user
        amount = request.data.get('amount')
        email = user.email
        callback_url = f"{request.build_absolute_uri(reverse('payment_verify'))}?user_id={user.id}"
        payment_response = initialize_payment(email, amount, callback_url)
        if payment_response['status']:
            return Response({'authorization_url': payment_response['data']['authorization_url']})
        return Response({'error': 'Payment initialization failed'}, status=status.HTTP_400_BAD_REQUEST)
            

class PaymentVerificationView(APIView):
    authentication_classes = ()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request):
        reference = request.GET.get('reference', None)
        user_id = request.GET.get('user_id', None)

        if reference is None or user_id is None:
            return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        
        verification_response = verify_payment(reference)
        if verification_response['status']:
            # Save the payment record
            user = CustomUser.objects.get(id= user_id)
            PaymentRecord.objects.create(
                user = user,
                amount=verification_response['data']['amount'] / 100,
                reference=reference,
                status='success'
            )
            return Response({'message': 'Payment successful'})
        return Response({'error': 'Payment verification failed'}, status=status.HTTP_400_BAD_REQUEST)
