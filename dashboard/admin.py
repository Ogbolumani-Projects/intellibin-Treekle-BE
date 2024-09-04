from django.contrib import admin
from .models import *
from .sensor_data import SensorData
# Register your models here.
admin.site.register(
    [WasteBin, WastePickUp, BinCompartment, SensorData]
)
