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
from .serializers import *
from django.http import Http404, JsonResponse
from .models import *
from rest_framework import viewsets
from rest_framework.decorators import action
from administration.serializers import *
from dashboard.sensor_data import SensorData



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
    

# class DashboardParameterView(APIView):

#     def post(self, request, *args, **kwargs):
#         # Accessing query parameters
#         param1 = request.query_params.get('param1')
#         param2 = request.query_params.get('param2')

#         # Accessing data from the request body
#         field1 = request.data.get('field1')
#         field2 = request.data.get('field2')

#         # Example logic to use both query params and request body data
#         if not field1 or not field2:
#             return Response({'error': 'Field1 and Field2 are required.'}, status=status.HTTP_400_BAD_REQUEST)

#         # You can include logic here that uses both query parameters and request body data
#         # For instance, saving data to the database or performing other operations

#         return Response({
#             'query_param1': param1,
#             'query_param2': param2,
#             'field1': field1,
#             'field2': field2
#         }, status=status.HTTP_201_CREATED)

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
        
class SaveBinData(APIView):

    # this is creating a new bin

    # in actuality it should update the bin
    serializer_class = WasteBinSerializer
    def post(self, request, pk):

        waste_bin = get_object_or_404(WasteBin.objects.all(),pk=pk)

        serializer = self.serializer_class(waste_bin,data=request.query_params, partial=True)
        if serializer.is_valid():
            data = serializer.save()

            return Response (serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)



def record_sensor_data(request):
    if request.method == 'GET':
        bin_id = request.GET.get('bin_id')
        waste_height = request.GET.get('waste_height')
        temperature = request.GET.get('temperature')
        humidity = request.GET.get('humidity')
        weight = request.GET.get('weight')
        batt_value = request.GET.get('batt_value')
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        # weather_condition = request.GET.get('weather_condition')

        if all([bin_id, waste_height, temperature, humidity, weight, batt_value, latitude, longitude]):
            try:
                waste_height = float(waste_height)
                temperature = float(temperature)
                humidity = float(humidity)
                weight = float(weight)
                batt_value = float(batt_value)
                latitude = float(latitude)
                longitude = float(longitude)
                
                # Save data to the database
                SensorData.objects.create(
                    bin_id=bin_id,
                    waste_height=waste_height,
                    temperature=temperature,
                    humidity=humidity,
                    weight=weight,
                    batt_value=batt_value,
                    latitude=latitude,
                    longitude=longitude,
                )

                sensor_data = SensorData.objects.all().values(
                    'bin_id', 'waste_height', 'temperature', 'humidity', 
                    'weight', 'batt_value', 'latitude', 'longitude')
                data_list = list(sensor_data)                
                return JsonResponse({'status': 'success', 'message': 'Sensor data recorded successfully.'}, data_list, safe=False)
            
            except ValueError as e:
                return JsonResponse({'status': 'error', 'message': f'Invalid value: {str(e)}'})
        
        else:
            return JsonResponse({'status': 'error', 'message': 'Missing required parameters.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

