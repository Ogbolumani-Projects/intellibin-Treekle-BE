from django.shortcuts import render

# Create your views here.
from authservice.models import *
from dashboard.models import *
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .serializers import *

class UserPanelViewSet(ModelViewSet):

    permission_classes = (IsAdminUser,)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class AdminWasteBinRequest(ModelViewSet):
    queryset = WasteBinRequest.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = WasteRequestSerialzier
        


class WasteBinAdmin(ModelViewSet):
    pass