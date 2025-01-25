from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    user_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

    def __str__(self):
        return self.user_id  # Or use user_id if you prefer