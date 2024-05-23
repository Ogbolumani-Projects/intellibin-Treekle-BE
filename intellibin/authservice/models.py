from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
# from django.contrib.auth.password_validation import validate_password


class CustomUser(AbstractUser):
    pass
# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError(_("Users must have a valid email address"))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

# class User(AbstractBaseUser):
#     email = models.EmailField(max_length=255, unique=True)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=30)
#     date_of_birth = models.CharField(max_length=30)
#     address = models.CharField(max_length=255)
#     phone_number = models.IntegerField(unique=True)
#     no_of_bins = models.IntegerField
#     # is_active = models.BooleanField(default=True)
#     # is_staff = models.BooleanField(default=False)
#     # is_superuser = models.BooleanField(default=False)
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']
    
#     objects = CustomUserManager()
    
#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'
    
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     # Add additional user profile fields here (e.g., preferred pickup day, bin type)
#     preferred_pickup_day = models.CharField(max_length=10, choices=(('MONDAY', 'Monday'), ('TUESDAY', 'Tuesday'), ('WEDNESDAY', 'Wednesday'), ('THURSDAY', 'Thursday'), ('FRIDAY', 'Friday')), blank=True)
#     bin_type = models.CharField(max_length=20, choices=(('ORGANIC', 'Organic'), ('RECYCLABLE', 'Recyclable'), ('GENERAL', 'General')), blank=True)
