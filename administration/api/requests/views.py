from datetime import datetime, timezone
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from authservice.models import CustomUser
from dashboard.models import WastePickUp, waste_pickup_status
from dashboard.serializers import WastePickRequestSerializer
from django.utils.dateparse import parse_datetime
from drf_spectacular.utils import extend_schema


class PendingPickupRequestsView(ListAPIView):
    queryset = WastePickUp.objects.all()
    serializer_class = WastePickRequestSerializer
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('date_created',)
    ordering = ['-date_created']

    def get_queryset(self):
        return self.get_queryset(status='Pending')


class ConfirmedPickupRequestsView(ListAPIView):
    queryset = WastePickUp.objects.all()
    serializer_class = WastePickRequestSerializer
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('date_created',)
    ordering = ['-date_created']

    def get_queryset(self):
        return self.get_queryset(status='Confirmed')


class FulfilledPickupRequestsView(ListAPIView):
    queryset = WastePickUp.objects.all()
    serializer_class = WastePickRequestSerializer
    authentication_classes = (JWTTokenUserAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (OrderingFilter,)
    ordering_fields = ('date_created',)
    ordering = ['-date_created']

    def get_queryset(self):
        return self.get_queryset(status='Picked up')


@extend_schema(
    request=WastePickRequestSerializer,
    responses=None
)
@api_view(['PUT',])
@authentication_classes((JWTTokenUserAuthentication,))
@permission_classes((IsAuthenticated,))
def update_pickup_status_request(request, id):
    try:
        pickup_request = WastePickUp.objects.get(id=id)
    except WastePickUp.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    status = request.data['status']
    available_status = [k for k, v in waste_pickup_status]
    if status in available_status:
        pickup_request.status = status
    else:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    if status == 'Confirmed':
        if 'pickup_date' in request.data:
            pickup_date = request.data['pickup_date']
            pickup_request.pickup_date_time = parse_datetime(pickup_date)
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    elif status == 'Picked up':
        pickup_request.date_picked = datetime.now(timezone.utc)
        # TODO: REWARD USER

    pickup_request.save()

    serializer = WastePickRequestSerializer(pickup_request)
    return Response(serializer.data)
