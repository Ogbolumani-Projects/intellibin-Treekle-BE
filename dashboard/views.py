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
from .models import SaveSensorData

from rest_framework import viewsets
from rest_framework.decorators import action
from administration.serializers import *
import logging



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
        

logger = logging.getLogger(__name__)

class RecordSensorData(APIView):
    """
    API endpoint that allows sensor data to be recorded via GET requests.
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'bin_id',
                openapi.IN_QUERY,
                description="Bin ID",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'waste_height',
                openapi.IN_QUERY,
                description="Waste height",
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
                required=True
            ),
            openapi.Parameter(
                'temperature',
                openapi.IN_QUERY,
                description="Temperature",
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
                required=True
            ),
            openapi.Parameter(
                'humidity',
                openapi.IN_QUERY,
                description="Humidity",
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
                required=True
            ),
            openapi.Parameter(
                'weight',
                openapi.IN_QUERY,
                description="Weight",
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
                required=True
            ),
            openapi.Parameter(
                'batt_value',
                openapi.IN_QUERY,
                description="Battery value",
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
                required=True
            ),
            openapi.Parameter(
                'latitude',
                openapi.IN_QUERY,
                description="Latitude",
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
                required=True
            ),
            openapi.Parameter(
                'longitude',
                openapi.IN_QUERY,
                description="Longitude",
                type=openapi.TYPE_NUMBER,
                format=openapi.FORMAT_FLOAT,
                required=True
            ),
        ],
         responses={
            200: openapi.Response(
                'Success',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING),
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_OBJECT, properties={
                                'bin_id': openapi.Schema(type=openapi.TYPE_STRING),
                                'date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                'time': openapi.Schema(type=openapi.TYPE_STRING, format='time'),
                                'waste_height': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                                'temperature': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                                'humidity': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                                'weight': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                                'batt_value': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                                'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                                'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
                                'weather_condition': openapi.Schema(type=openapi.TYPE_STRING),
                            })
                        ),
                    }
                )
            ),
            400: 'Bad Request',
            500: 'Internal Server Error'
        }
    )
    def get(self, request, format=None):
        """
        Handle GET request to record sensor data.
        """
        try:
            bin_id = request.GET.get('bin_id')
            waste_height = request.GET.get('waste_height')
            temperature = request.GET.get('temperature')
            humidity = request.GET.get('humidity')
            weight = request.GET.get('weight')
            batt_value = request.GET.get('batt_value')
            latitude = request.GET.get('latitude')
            longitude = request.GET.get('longitude')

            # Validate required parameters
            required_params = [
                ('bin_id', bin_id),
                ('waste_height', waste_height),
                ('temperature', temperature),
                ('humidity', humidity),
                ('weight', weight),
                ('batt_value', batt_value),
                ('latitude', latitude),
                ('longitude', longitude)
            ]

            missing_params = [name for name, value in required_params if value is None]
            if missing_params:
                message = f"Missing required parameters: {', '.join(missing_params)}"
                logger.warning(message)
                return Response({'status': 'error', 'message': message}, status=status.HTTP_400_BAD_REQUEST)

            # Convert parameters to appropriate types
            try:
                waste_height = float(waste_height)
                temperature = float(temperature)
                humidity = float(humidity)
                weight = float(weight)
                batt_value = float(batt_value)
                latitude = float(latitude)
                longitude = float(longitude)
            except ValueError as ve:
                message = f"Invalid data type: {ve}"
                logger.error(message)
                return Response({'status': 'error', 'message': message}, status=status.HTTP_400_BAD_REQUEST)

            # Create SensorData instance
            sensor_data = SaveSensorData.objects.create(
                bin_id=bin_id,
                waste_height=waste_height,
                temperature=temperature,
                humidity=humidity,
                weight=weight,
                batt_value=batt_value,
                latitude=latitude,
                longitude=longitude,
                # 'date' and 'time' are auto-set
                weather_condition='clear'  # Default or retrieve if provided
            )

            serializer = SensorDataSerializer(sensor_data)

            logger.info(f"Sensor data recorded: {sensor_data}")
            return Response({
                'status': 'success',
                'message': 'Sensor data recorded successfully.',
                'data': [serializer.data]  # Returning as a list
            }, status=status.HTTP_200_OK)

        except Exception as e:
            message = f"An unexpected error occurred: {e}"
            logger.exception(message)
            return Response({'status': 'error', 'message': message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        
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
    





