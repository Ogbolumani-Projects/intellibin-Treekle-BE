from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User, AbstractUser
from django.contrib.auth.password_validation import validate_password
# Create your models here.


class CustomManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, and password.
        """
        if not email:
            raise ValueError("Users must have a valid email address ")
        user = self.model(
            email=self.normalize_email(email),

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, and password.
        """
        if not email:
            raise ValueError("Users must have a valid email address ")

        user = self.create_user(
            email,
            password=password,
        )
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser, PermissionsMixin):
    username = None
    full_name = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.TextField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    # every profile must belong one to user
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE)
    bio = models.TextField(null=True)
