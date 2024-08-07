from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from authservice.models import CustomUser
from dashboard.models import WastePickUp
from dashboard.serializers import WastePickRequestSerializer


class PendingPickupRequestsView(ListAPIView):
    queryset = WastePickUp.objects.all()
    serializer_class = WastePickRequestSerializer
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('date_created',)
    ordering = ['-date_created']

    def get_queryset(self):
        return self.get_queryset(pending=True)


class ConfirmedPickupRequestsView(ListAPIView):
    queryset = WastePickUp.objects.all()
    serializer_class = WastePickRequestSerializer
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('date_created',)
    ordering = ['-date_created']

    def get_queryset(self):
        return self.get_queryset(confirmed=True)


class FulfilledPickupRequestsView(ListAPIView):
    queryset = WastePickUp.objects.all()
    serializer_class = WastePickRequestSerializer
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('date_created',)
    ordering = ['-date_created']

    def get_queryset(self):
        return self.get_queryset(confirmed=True)
