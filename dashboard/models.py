from typing import Iterable
from django.db import models
from authservice.models import *
from django.db.models import Sum, Avg, Count

waste_category = [
    ("RECYCLABLE", "RECYCLABLE"),
    ("NON_RECYCLABLE", "NON_RECYCLABLE")
]


class BinCompartment(models.Model):

    parent_bin = models.ForeignKey(
        "WasteBin", related_name="compartments", on_delete=models.CASCADE)
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
        return self.compartments.filter(user=self.user, bin_level__gt=50).count()

    @property
    def half_bins(self):
        return self.compartments.filter(user=self.user, bin_level=50).count()

    @property
    def spacious_bins(self):
        return self.compartments.filter(user=self.user, bin_level__lt=45).count()


waste_pickup_status = [
    ("Pending", "Pending"),
    ("Confirmed", "Confirmed"),
    ("Picked up", "Picked up"),
    ("Cancelled", "Cancelled"),
]


class WastePickUp(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    waste_type = models.CharField(choices=waste_category, max_length=253)
    parent_bin = models.ForeignKey(WasteBin, on_delete=models.CASCADE)
    reward_gained = models.IntegerField(null=True)
    status = models.CharField(
        choices=waste_pickup_status, max_length=253, default='Pending')
    pickup_date_time = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_picked = models.DateTimeField()

    def gain_reward_points(self):

        compartments = self.parent_bin.comparments.filter(
            waste_category="RECYCLABLE")
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


# class wasteBin(models.Model):
#     RECYCLABLE = 'recyclable'
#     NON_RECYCLABLE = 'non-recyclable'
#     WASTE_TYPES = [
#         (RECYCLABLE, 'Recyclable'),
#         (NON_RECYCLABLE, 'Non-Recyclable'),
#     ]
#     type_of_waste = models.CharField(max_length=20, choices=WASTE_TYPES)
#     temperature = models.FloatField(null=True)
#     location = models.TextField(null=True)
#     bin_level = models.IntegerField(null=True)
#     battery_level = models.IntegerField(null=True)
#     charge_status = models.BooleanField(null=True)
#     power_consumption = models.FloatField(null=True)
#     battery_status = models.IntegerField(null=True)
#     is_active = models.BooleanField(default=False)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

#     def reward_points_sum_bin_count(self):

#         return wasteBin.objects.filter(user=self.user).aggregate(
#             Sum("reward_points"), Count('id')
#         )

#     def full_bins(self):
#         return wasteBin.objects.filter(user=self.user, bin_level__gt=50).count()

#     def half_bins(self):
#         return wasteBin.objects.filter(user=self.user, bin_level=50).count()


#     def spacious_bins(self):
#         return wasteBin.objects.filter(user=self.user, bin_level__lt=45).count()


# class wastePickUp(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     type_of_waste = models.ForeignKey(on_delete=models.CASCADE)
#     confirmed = models.BooleanField(default=False)
#     pending = models.BooleanField(default=True)
#     picked_up = models.BooleanField(default=False)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_picked = models.DateTimeField()


# class wasteBinRequests(models.Model):
#     pass

# class wasteHistory(models.Model):
#     bin = models.ForeignKey(wasteBin, on_delete=models.CASCADE)
#     #date_time = models.DateTimeField(auto_now_add=True)
#     quantity = models.IntegerField()
#     points = models.IntegerField()
#     status = models.CharField(max_length=20)
#     #type = models.CharField(max_length=20)
#     date_created = models.DateTimeField(auto_now_add=True)
#     type_of_waste = models.ForeignKey(wasteCategory, on_delete=models.CASCADE)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
