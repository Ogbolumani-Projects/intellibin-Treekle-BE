from typing import Iterable
from django.db import models
from authservice.models import *
from django.db.models import Sum, Avg, Count

waste_category = [
        ("RECYCLABLE", "RECYCLABLE"),
        ("NON_RECYCLABLE", "NON_RECYCLABLE")
    ]

class BinCompartment(models.Model):
    
    parent_bin = models.ForeignKey("WasteBin", related_name="compartments", on_delete=models.CASCADE)
    type_of_waste = models.CharField(choices=waste_category, max_length=20)
    temperature = models.FloatField(null=True)
    weight = models.FloatField(null=True, default=0)  
    bin_level = models.IntegerField(null=True)
   
class BinLocation(models.Model):

    location = models.TextField(null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    class Meta:
        abstract = True

class WasteBin(BinLocation):
    
    reward_points = models.IntegerField(null=True, default=0)
    
    battery_level = models.IntegerField(null=True)
    charge_status = models.BooleanField(null=True)
    power_consumption = models.FloatField(null=True)
    battery_status = models.IntegerField(null=True)
    picked_up = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)


    def reward_points_sum_bin_count(self):
        
        return self.compartments.filter(user=self.user).aggregate(
            Sum("reward_points"), Count('id')
        )

    @property
    def full_bins(self):   
        # return self.compartments.filter(user=self.user, bin_level__gt=50).count()
        return self.compartments.filter(bin_level__gt=50).count()

    @property
    def half_bins(self):
        # return self.compartments.filter(user=self.user, bin_level=50).count()
        return self.compartments.filter(bin_level=50).count()

    @property
    def spacious_bins(self):
        # return self.compartments.filter(user=self.user, bin_level__lt=45).count()
        return self.compartments.filter(bin_level__lt=45).count()
    
    @property
    def bin_level(self):
        return self.compartments.filter(type_of_waste="NON_RECYCLABLE")[0].bin_level
    
    @property
    def weight(self):
        return self.compartments.filter(type_of_waste="RECYCLABLE")[0].weight
    

    def __str__(self):
        return f"{self.device_id} - {self.reading} at {self.timestamp}"
    
class WastePickUp(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    waste_type = models.CharField(choices=waste_category, max_length=20)
    parent_bin = models.ForeignKey(WasteBin, on_delete=models.CASCADE)
    reward_gained = models.IntegerField(null=True)
    completed = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)
    picked_up = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_picked = models.DateTimeField()


    def gain_reward_points(self):

        compartments = self.parent_bin.compartments.filter(type_of_waste="RECYCLABLE")          
        # assumption is that a single comparment
        if compartments[0].weight > 50:
            self.parent_bin.reward_points += 10
            self.reward_gained = 10
            self.parent_bin.save()
        
    
    def save(self) -> None:
        super().save()
        self.gain_reward_points()

        
class WasteBinRequest(BinLocation):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_requested = models.DateTimeField(auto_now_add=True, null=True)
    approved = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)
    
class SaveSensorData(models.Model):
    bin_id = models.CharField(max_length=120)
    time = models.TimeField(auto_now_add=True, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    humidity = models.FloatField()
    waste_height = models.FloatField()
    temperature = models.FloatField()
    weight = models.FloatField()
    batt_value = models.FloatField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    weather_condition = models.CharField(max_length=255, default="clear")

    def __str__(self):
        return f"{self.bin_id} - {self.date} {self.time}"
    