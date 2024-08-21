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
from django.http import Http404
from .models import *
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
    serializer_class = AdminWasteBinSerializer
    
    def post(self,request):
        serializer = self.serializer_class(data=request.query_params)
        if serializer.is_valid():

            #data = serializer.create(serializer.validated_data)
            data = serializer.save()
            
        return Response(data, status=status.HTTP_201_CREATED)

    def put(self, request, pk):

        waste_bin = get_object_or_404(WasteBin, lpk=pk)
        serializer = self.serializer_class(waste_bin,data=request.query_params, partial=True)

        if serializer.is_valid():
            data = serializer.save()
        
        return Response (data, status=status.HTTP_200_OK)