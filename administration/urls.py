from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"users", UserPanelViewSet, basename="users")
router.register(r"wastebin-request", AdminWasteBinRequest, basename="wastebin-request")
router.register(r"waste-bin", WasteBinAdmin, basename="admin-waste-bin")


urlpatterns = [
    path("bin-token/", GenerateSmartBinToken.as_view(), name="bin-token")
    
]+router.urls