from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register("pickups", WasteBinPickupView, basename="wastebin pickup")
router.register("dashboard", WasteBinViewset, basename="dashboard")
router.register("bin-request", WasteBinRequest, basename="bin-request")
# router.register('record-sensor-data', RecordSensorData, basename="record-sensor-data")

urlpatterns = [
    path('record-sensor-data/', RecordSensorData.as_view(), name='record_sensor_data'),
]+router.urls
