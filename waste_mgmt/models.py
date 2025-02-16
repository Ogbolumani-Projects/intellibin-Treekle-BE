from django.db import models

# Create your models here.

import uuid

class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    # Add more fields as needed

class Bin(models.Model):
    bin_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    capacity = models.FloatField()
    current_level = models.FloatField(default=0)
    batt_value = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    temperature = models.FloatField()
    waste_height = models.FloatField()
    humidity = models.FloatField()
    weight = models.FloatField()

class WasteData(models.Model):
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)




    # https://server.com/api/v1/get_sensor_data/?bin_id=1&waste_height=1.0&temperature=1.0&humidity=1.0&weight=1.0&batt_value=1.0&latitude=1.0&longitude=1.0