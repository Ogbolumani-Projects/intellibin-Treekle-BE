from django.db import models

# Create your models here.
from django.conf import settings

class Bin(models.Model):
    bin_id = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    waste_type = models.CharField(max_length=50)
    capacity = models.FloatField()

    def __str__(self):
        return f"Bin {self.bin_id} ({self.waste_type})"

class WasteData(models.Model):
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE)
    fill_level = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Waste Data for Bin {self.bin.bin_id} at {self.timestamp}"