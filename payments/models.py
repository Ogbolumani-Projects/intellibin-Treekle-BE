from django.db import models

# Create your models here.
from django.conf import settings

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_ref = models.CharField(max_length=255, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    # Add other fields as needed (e.g., payment_method, status)

    def __str__(self):
        return f"Payment of {self.amount} by {self.user.username} on {self.payment_date}"
