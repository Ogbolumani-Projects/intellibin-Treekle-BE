from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter
from .views import record_sensor_data

router = DefaultRouter()
router.register("pickups", WasteBinPickupView, basename="wastebin pickup")
router.register("dashboard", WasteBinViewset, basename="dashboard")
router.register("bin-request", WasteBinRequest, basename="bin-request")

urlpatterns = [
    path("save_data/<int:pk>/", SaveBinData.as_view(), name='save_bin_data'),
    path('api/record/', record_sensor_data, name='record_sensor_data'),

    
]+router.urls
