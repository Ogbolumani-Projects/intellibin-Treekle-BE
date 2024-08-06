from django.db import models
from authservice.models import *
from django.db.models import Sum, Avg, Count

class wasteCategory(models.Model):
    # name = models.CharField(max_length=500)
    # def __str__(self):
    #     return self.name
    RECYCLABLE = 'recyclable'
    NON_RECYCLABLE = 'non-recyclable'

    WASTE_TYPES = [
        (RECYCLABLE, 'Recyclable'),
        (NON_RECYCLABLE, 'Non-Recyclable'),
    ]

    name = models.CharField(max_length=20, choices=WASTE_TYPES)

# Create your models here.
class wasteBin(models.Model):
    #type_of_waste = models.ForeignKey(wasteCategory, on_delete=models.CASCADE)
    temperature = models.FloatField(null=True)
    location = models.TextField(null=True)
    bin_level = models.IntegerField(null=True)
    battery_level = models.IntegerField(null=True)
    charge_status = models.BooleanField(null=True)
    power_consumption = models.FloatField(null=True)
    battery_status = models.IntegerField(null=True)
    is_active = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def reward_points_sum_bin_count(self):
        
        return wasteBin.objects.filter(user=self.user).aggregate(
            Sum("reward_points"), Count('id')
        )

    def full_bins(self):
        return wasteBin.objects.filter(user=self.user, bin_level__gt=50).count()
    
    def half_bins(self):
        return wasteBin.objects.filter(user=self.user, bin_level=50).count()


    def spacious_bins(self):
        return wasteBin.objects.filter(user=self.user, bin_level__lt=45).count()


class wastePickUp(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type_of_waste = models.ForeignKey(wasteCategory, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)
    picked_up = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_picked = models.DateTimeField()


class wasteBinRequests(models.Model):
    pass

class wasteHistory(models.Model):
    bin = models.ForeignKey(wasteBin, on_delete=models.CASCADE)
    #date_time = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    points = models.IntegerField()
    status = models.CharField(max_length=20)
    #type = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    type_of_waste = models.ForeignKey(wasteCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    