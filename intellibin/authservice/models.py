from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.contrib.auth.password_validation import validate_password
# Create your models here.


class CustomManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have a valid email address ")
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have a valid email address ")
        
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
        raise ValueError("Users must have a valid email address ")


class CustomUser(AbstractBaseUser, PermissionsMixin): 
    firstname = models.CharField(max_length=50, null=True)
    lastname = models.CharField(max_length=50,null=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    verified = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True)
    phone_number = models.IntegerField(default='1234')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["date_of_birth"]

    def __str__(self):
        return self.email
        
    
class UserProfile(models.Model):
    user = models.OneToOneField("CustomUser", on_delete=models.CASCADE) # every profile must belong one to user
    bio = models.TextField(null=True)
    

    