from django.db import models

# Create your models here.
class User(models.Model):
    firstname = models.CharField(max_length= 255)
    lastname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=15)
    password = models.CharField(max_length=25)
    password2 = models.CharField(max_length=25)
    #gender = models.CharField(type= bool)
    address = models.TextField(max_length=255)
    phone_number = models.CharField(max_length= 25)
    dob = models.DateField(null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2, default=3)
    otp_max_out = models.DateTimeField(blank=True, null=True)
