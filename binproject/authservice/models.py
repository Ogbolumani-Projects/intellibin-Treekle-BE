from django.db import models

# Create your models here.
class UserRegister(models.Model):
    email = models.CharField(max_length=255)
class User(models.Model):
    user_id = models.CharField(max_length= 255)
    first_name = models.CharField(max_length= 255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length= 25)
    dob = models.DateField(null=True, blank=True)
    email_address = models.CharField(max_length=255)
    address = models.TextField(max_length=255)
    password = models.CharField(max_length=25)
    password2 = models.CharField(max_length=25)
    #gender = models.CharField(type= bool)
    
    # otp = models.CharField(max_length=6, null=True, blank=True)
    # otp_expiry = models.DateTimeField(blank=True, null=True)
    # max_otp_try = models.CharField(max_length=2, default=3)
    # otp_max_out = models.DateTimeField(blank=True, null=True)
