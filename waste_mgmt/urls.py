# waste_mgmt/urls.py
from django.urls import path
from .views import BinViewSet, WasteDataViewSet, receive_iot_data

urlpatterns = [
    path('bins/', BinViewSet.as_view({'get': 'list'}), name='bin-list'),
    path('wastedata/', WasteDataViewSet.as_view({'get': 'list'}), name='waste-data'),
    path('iot-data/', receive_iot_data, name='iot-data'),
]