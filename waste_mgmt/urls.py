from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'bins', BinViewSet, basename='bin')
router.register(r'bin-data', WasteDataViewSet, basename='bin-data')
router.register(r'weather-data', WeatherDataViewSet, basename='weather-data')
router.register(r'customer-profiles', CustomerProfileViewSet, basename='customer-profile')
router.register(r'employee-profiles', EmployeeProfileViewSet, basename='employee-profile')
router.register(r'admin-profiles', AdminProfileViewSet, basename='admin-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('get-bin-data/', WasteDataReceiveView.as_view(), name='get-bin-data'),
    path('customer/bins/', CustomerBinsView.as_view(), name='customer-bins'),

]