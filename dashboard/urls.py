from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("pickups", WasteBinPickupView, basename="wastebin pickup")
router.register("dashboard", WasteBinViewset, basename="dashboard")
router.register("bin-request", WasteBinRequest, basename="bin-request")
router.register(r'dashboard-reading', DashboardParameterViewSet, basename='dashboard-reading')
urlpatterns = [
    
]+router.urls

