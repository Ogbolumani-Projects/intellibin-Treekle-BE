from django.db import models
from authservice.models import *


NOTIFICATION_RECIPIENT_CHOICES = (
    ("Admin", "Admin"),
    ("User", "User"),
)

# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=255)
    msg = models.TextField()
    recipient = models.CharField(max_length=5, choices=NOTIFICATION_RECIPIENT_CHOICES)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    

