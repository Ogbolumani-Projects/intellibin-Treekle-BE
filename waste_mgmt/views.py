from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class BinViewSet(viewsets.ModelViewSet):
    queryset = Bin.objects.all()
    serializer_class = BinSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer']
    search_fields = ['bin_id', 'location']
    ordering_fields = ['bin_id', 'location', 'customer']

    @action(detail=True, methods=['post'])
    def assign_customer(self, request, pk=None):
        bin = self.get_object()
        customer_id = request.data.get('customer_id')
        if not customer_id:
            return Response({'error': 'customer_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            customer = User.objects.get(pk=customer_id)
        except User.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
        bin.customer = customer
        bin.save()
        return Response(BinSerializer(bin).data)

    @action(detail=True, methods=['post'])
    def unassign_customer(self, request, pk=None):
        bin = self.get_object()
        bin.customer = None
        bin.save()
        return Response(BinSerializer(bin).data)

class WasteDataViewSet(viewsets.ModelViewSet):
    queryset = WasteData.objects.all()
    serializer_class = WasteDataSerializer

class WeatherDataViewSet(viewsets.ModelViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer

class CustomerBinsView(generics.ListAPIView):
    serializer_class = BinSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Bin.objects.filter(customer=user)
    
class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer

class EmployeeProfileViewSet(viewsets.ModelViewSet):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer

class AdminProfileViewSet(viewsets.ModelViewSet):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WasteDataReceiveView(APIView):
    def get(self, request):
        bin_id = request.query_params.get('bin_id')
        waste_height = request.query_params.get('waste_height')
        temperature = request.query_params.get('temperature')
        humidity = request.query_params.get('humidity')
        weight = request.query_params.get('weight')
        batt_value = request.query_params.get('batt_value')
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        fill_level = request.query_params.get('fill_level')

        if not bin_id:
            return Response({'error': 'bin_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        bin = get_object_or_404(Bin, bin_id=bin_id)

        data = {
            'bin': bin.id,
            'waste_height': waste_height,
            'temperature': temperature,
            'humidity': humidity,
            'weight': weight,
            'batt_value': batt_value,
            'latitude': latitude,
            'longitude': longitude,
            'fill_level': fill_level,
        }

        serializer = WasteDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 
                            {'message': 'Waste data received successfully',
                             'customer': bin.customer.username,
                             'data': serializer.data,},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
