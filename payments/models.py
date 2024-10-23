from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import secrets
from .paystack import Paystack
from authservice.models import *


TIER_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]

# class SubscriptionTier(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()

class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tier = models.CharField(max_length=20, choices= TIER_CHOICES)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    
class UserWallet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    currency = models.CharField(max_length=50, default='NGN')
    created_at = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.user.__str__()
    

class PaymentRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)  # 'reward_points', 'cash', 'card'
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='pending')
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"Payment: {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref

        super().save(*args, **kwargs)
