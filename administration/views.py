from django.shortcuts import render

# Create your views here.
from authservice.models import *
from dashboard.models import *
from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *

class UserPanelViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = CustomUser.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["verified"]
    serializer_class = UserSerializer


class AdminWasteBinRequest(ModelViewSet):
    queryset = WasteBinRequest.objects.all()
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["approved", "pending"]
    serializer_class = WasteRequestSerializer
        


class WasteBinAdmin(ModelViewSet):
    queryset = WasteBin.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = AdminWasteBinSerializer
    

class GenerateSmartBinToken(APIView):
    permission_classes = [IsAdminUser]
    http_method_names = ["get"]
    def get(self, request):
        token, created = Token.objects.get_or_create(user=request.user)
        print(token.key)
        return Response(token.key)