from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"users", UserPanelViewSet, basename="users")
router.register(r"wastebin-request", AdminWasteBinRequest, basename="wastebin-request")




urlpatterns = [
    
]+router.urls