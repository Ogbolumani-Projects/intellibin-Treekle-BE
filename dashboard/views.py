from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import *
from django.http import Http404, JsonResponse
from .models import *
from .models import SensorData

from rest_framework import viewsets
from rest_framework.decorators import action
from administration.serializers import *



# is for the user to view details about their bins
class WasteBinViewset(ReadOnlyModelViewSet):
    queryset = WasteBin.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = WasteBinSerializer


    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
# user can request for a bin, approval or actual bin creation is done on the admin
class WasteBinRequest(ModelViewSet):
    queryset = WasteBinRequest
    serializer_class = RequestWasteBinSerializer
    
    permission_classes = (IsAuthenticated,)
    #methods allowed :  get : user can view all requests, post: create a new bin request, delete: to delete a request
    http_method_names = ['get','post', 'delete'] 


# is to request for a bin pickup
class WasteBinPickupView(ModelViewSet):
    queryset = WastePickUp.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["completed", "pending", "waste_type"]
    serializer_class = WastePickRequestSerializer
    http_method_names = ['get','post']


    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    

class DashboardParameterViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def save_data(self, request):
        serializer = DashboardParameterSerializer(data=request.query_params)
        if serializer.is_valid():
            # Perform the save operation
            data = serializer.validated_data
            BinCompartment.objects.update_or_create(
                id=data['id'],
                defaults={
                    'reward_points': data['reward_points'],
                    'battery_level': data['battery_level'],
                    'charge_status': data['charge_status'],
                    'power_consumption': data['power_consumption'],
                    'temperature': data['temperature'],
                    'weight': data['weight'],
                    'bin_level': data['bin_level']
                }
            )
            return Response({'status': 'success', 'message': 'Data saved successfully'})
        else:
            return Response({'status': 'error', 'message': serializer.errors}, status=400)
        

class RetrieveSensorData(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('bin_id', openapi.IN_QUERY, description="Bin ID", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('date', openapi.IN_QUERY, description="Date of reading", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=True),
            # Add other parameters as needed
        ],
        responses={
            200: 'Success',
            400: 'Bad Request'
        }
    )
    def get(self, request, format=None):
        bin_id = request.GET.get('bin_id')
        # date = request.GET.get('date')
        waste_height = request.GET.get('waste_height')
        temperature = request.GET.get('temperature')
        humidity = request.GET.get('humidity')
        weight = request.GET.get('weight')
        batt_value = request.GET.get('batt_value')
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')

        # Retrieve other parameters...

        if not bin_id or not date:
            return Response({'status': 'error', 'message': 'Missing required parameters.'},
                            status=status.HTTP_400_BAD_REQUEST)

        sensor_data = SensorData.objects.filter(bin_id=bin_id, date=date)
        data_list = list(sensor_data.values())
        return Response({'status': 'success', 'data': data_list}, status=status.HTTP_200_OK)

class RecordSensorData(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('bin_id', openapi.IN_QUERY, description="Bin ID", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('time', openapi.IN_QUERY, description="Time of reading", type=openapi.TYPE_STRING, format=openapi.FORMAT_TIME, required=True),
            openapi.Parameter('waste_height', openapi.IN_QUERY, description="Waste height", type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, required=True),
            openapi.Parameter('temperature', openapi.IN_QUERY, description="Temperature", type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, required=True),
            openapi.Parameter('humidity', openapi.IN_QUERY, description="Humidity", type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, required=True),
            openapi.Parameter('weight', openapi.IN_QUERY, description="Weight", type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, required=True),
            openapi.Parameter('batt_value', openapi.IN_QUERY, description="Battery value", type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, required=True),
            openapi.Parameter('latitude', openapi.IN_QUERY, description="Latitude", type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, required=True),
            openapi.Parameter('longitude', openapi.IN_QUERY, description="Longitude", type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, required=True),
            # openapi.Parameter('weather_condition', openapi.IN_QUERY, description="Weather condition", type=openapi.TYPE_STRING, required=True),
        ],
        responses={
            200: openapi.Response('Success', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING),
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )),
            400: 'Bad Request'
        }
    )
    def get(self, request, format=None):
        bin_id = request.GET.get('bin_id')
        time = request.GET.get('time')
        waste_height = request.GET.get('waste_height')
        temperature = request.GET.get('temperature')
        humidity = request.GET.get('humidity')
        weight = request.GET.get('weight')
        batt_value = request.GET.get('batt_value')
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        # weather_condition = request.GET.get('weather_condition')

        if not all([bin_id, time, waste_height, temperature, humidity, weight, batt_value, latitude, longitude]):
            return JsonResponse({'status': 'error', 'message': 'Missing required parameters.'}, status=400)

        try:
            # Convert values to appropriate types
            waste_height = float(waste_height)
            temperature = float(temperature)
            humidity = float(humidity)
            weight = float(weight)
            batt_value = float(batt_value)
            latitude = float(latitude)
            longitude = float(longitude)

            SensorData.objects.create(
                bin_id=bin_id,
                time=time,
                waste_height=waste_height,
                temperature=temperature,
                humidity=humidity,
                weight=weight,
                batt_value=batt_value,
                latitude=latitude,
                longitude=longitude,
                # weather_condition=weather_condition
            )

            sensor_data = SensorData.objects.filter(
                    'bin_id', 'waste_height', 'temperature', 'humidity', 
                    'weight', 'batt_value', 'latitude', 'longitude')
            data_list = list(sensor_data.values())                

            return JsonResponse({'status': 'success', 'message': 'Sensor data recorded successfully.'}, data_list, status=200)

        except ValueError as e:
            return JsonResponse({'status': 'error', 'message': f'Invalid value: {str(e)}'}, status=400)


        
# class SaveBinData(APIView):
#     def record_sensor_data(request):
#         if request.method == 'GET':
#             bin_id = request.GET.get('bin_id')
#             waste_height = request.GET.get('waste_height')
#             temperature = request.GET.get('temperature')
#             humidity = request.GET.get('humidity')
#             weight = request.GET.get('weight')
#             batt_value = request.GET.get('batt_value')
#             latitude = request.GET.get('latitude')
#             longitude = request.GET.get('longitude')
#             # weather_condition = request.GET.get('weather_condition')

#             if all([bin_id, waste_height, temperature, humidity, weight, batt_value, latitude, longitude]):
#                 try:
#                     waste_height = float(waste_height)
#                     temperature = float(temperature)
#                     humidity = float(humidity)
#                     weight = float(weight)
#                     batt_value = float(batt_value)
#                     latitude = float(latitude)
#                     longitude = float(longitude)
                
#                     # Save data to the database
#                     SensorData.objects.create(
#                         bin_id=bin_id,
#                     # date=date,
#                     # time=time,
#                         waste_height=waste_height,
#                         temperature=temperature,
#                         humidity=humidity,
#                         weight=weight,
#                         batt_value=batt_value,
#                         latitude=latitude,
#                         longitude=longitude,
#                         #weather_condition=weather_condition
#                     )
#                     sensor_data = SensorData.objects.all().values(
#                         'bin_id', 'waste_height', 'temperature', 'humidity', 
#                         'weight', 'batt_value', 'latitude', 'longitude')

#                     return JsonResponse({'status': 'success', 'message': 'Sensor data recorded successfully.'}, data_list, safe=False)
            
#                 except ValueError as e:
#                     return JsonResponse({'status': 'error', 'message': f'Invalid value: {str(e)}'})
        
#             else:
#                 return JsonResponse({'status': 'error', 'message': 'Missing required parameters.'})
    
#         return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

    # this is creating a new bin

    # in actuality it should update the bin
    # serializer_class = WasteBinSerializer
    # def post(self, request, pk):

    #     waste_bin = get_object_or_404(WasteBin.objects.all(),pk=pk)

    #     serializer = self.serializer_class(waste_bin,data=request.query_params, partial=True)
    #     if serializer.is_valid():
    #         data = serializer.save()

    #         return Response (serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors)
    





