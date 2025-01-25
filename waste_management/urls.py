from django.urls import path
from .views import WasteDataAPIView

urlpatterns = [
    path('waste-data/', WasteDataAPIView.as_view(), name='waste-data'),
]