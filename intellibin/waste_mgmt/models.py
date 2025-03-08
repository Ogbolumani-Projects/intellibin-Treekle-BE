from django.db import models
from django.contrib.auth.models import User

class Bin(models.Model):
    bin_id = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='inactive')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.bin_id

class WasteData(models.Model):
    bin_id = models.ForeignKey(Bin, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    fill_level = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    weight = models.FloatField()
    batt_value = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    waste_height = models.FloatField()

    def __str__(self):
        return f"{self.bin.bin_id} - {self.timestamp}"

class WeatherData(models.Model):
    location = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    condition = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.location} - {self.timestamp}"

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add custom fields for customers here
    location = models.CharField(max_length=300, default='Lagos')

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add custom fields for employees here
    location = models.CharField(max_length=300, default='Lagos')
    employee_id = models.CharField(max_length=255, default='ib_001001', unique=True)
    department = models.CharField(max_length=255, default='operations')

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add custom fields for admins here
    department = models.CharField(max_length=255, default='admin')
    location = models.CharField(max_length=300, default='Lagos')
    employee_id = models.CharField(max_length=255, default='ib_00010', unique=True)

# bin_id=1&waste_height=1.0&temperature=1.0&humidity=1.0&weight=1.0&batt_value=1.0&latitude=1.0&longitude=1.0&fill_level=50&bin=3
