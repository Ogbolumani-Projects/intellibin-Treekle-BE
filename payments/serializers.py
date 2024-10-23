from rest_framework import serializers
from .models import Subscription, PaymentRecord

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['tier']

class PaymentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRecord
        fields = ['amount', 'reference', 'status']