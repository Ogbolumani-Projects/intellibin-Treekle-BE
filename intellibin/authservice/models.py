from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class CustomUser(AbstractBaseUser ,PermissionsMixin):
    full_name = models.CharField(max_length= 255, default= 'Anyname')
    email = models.EmailField(
        verbose_name="email address",
        max_length= 255,
        unique=True,
        )
    verified = models.BooleanField(default=False)
    phone_number = models.IntegerField(default= '12345')
    password = models.CharField(max_length=255,default='defaultpassword')
    address = models.TextField(null= True)
    is_active = models.BooleanField(default= True)

    USERNAME_FIELD = ("email")
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
    