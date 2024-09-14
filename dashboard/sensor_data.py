from django.db import models

class SensorData(models.Model):
    bin_id = models.CharField(max_length=230)
    timestamp = models.DateTimeField(auto_now_add=True)
    waste_height = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    weight = models.FloatField()
    batt_value = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.bin_id} - {self.waste_height} - {self.temperature} - {self.weight} - {self.waste_height} - {self.batt_value} - {self.humidity} - {self.longitude} - {self.latitude} at {self.timestamp}"
    