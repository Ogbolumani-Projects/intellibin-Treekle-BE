from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .serializers import *
from .models import *
from authservice.models import *


from django.http.response import HttpResponse
from django.core.mail import send_mail
# Create your views here.

class DashBoardView(APIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        waste_bins = wasteBin.objects.filter(user=request.user) 
        # a list of bins        
        
        waste_bin_list = [  
            {
                'waste_bin': waste_bin
            }
            for waste_bin in waste_bins.values()
        ]


        return Response(
            {
                'user': request.user.fullname,
                'total_reward_point': waste_bins[0].reward_points_sum_bin_count(),
                'waste_bins':waste_bin_list,
                'full_bins':waste_bins[0].full_bins(),
                'half_bins':waste_bins[0].half_bins(),
                'other_bin_levels':waste_bins[0].spacious_bins()

            }
        )
    
    def post(self, request):
        pass

class WasteBinPickupView(APIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializers = WastePickRequestSerializer(data=request.data)
       
        if serializers.is_valid():
            waste_type =  wasteCategory.objects.get(name=serializers.data['type_of_waste'])
            print(waste_type)
            pickup = wastePickUp.objects.create(
                user = request.user,
                type_of_waste = waste_type,
                pending=True
            ).save()

            return Response(
                "Request Successful", status=status.HTTP_201_CREATED
            )   
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class WasteBinUpdateView(generics.UpdateAPIView):
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    pass

class BinView(APIView):
    def get(self, request):
        bins = wasteBin.objects.all()
        serializer = wasteBinSerializer(bins, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = wasteBinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestBinView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        location = request.data.get('location')
        # Send an email request for a bin (simplified example)
        send_mail(
            'Bin Request',
            f'User {request.user.username} has requested a bin at {location}.',
            'the.ayoadeborah@gmail.com',
            [email],
        )
        return Response({'message': 'Bin request sent successfully.'}, status=status.HTTP_200_OK)

class wasteBinListView(generics.ListCreateAPIView):
    queryset = wasteBin.objects.all()
    serializer_class = wasteBinSerializer
    permission_classes = [IsAuthenticated]

class BinDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = wasteBin.objects.all()
    serializer_class = wasteBinSerializer
    permission_classes = [IsAuthenticated]

class RequestPickupView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        bin_id = request.data.get('bin_id')
        waste_type = request.data.get('type')
        bin_instance = wasteBin.objects.get(id=bin_id)
        if bin_instance.fill_level < 50:
            return Response({'message': 'Cannot pickup at the moment.'}, status=status.HTTP_400_BAD_REQUEST)
        # if waste_type == 'recyclable' and bin_instance.recyclable_fill_level < 50:
        #     return Response({'message': 'Cannot pickup at the moment.'}, status=status.HTTP_400_BAD_REQUEST)
        # if waste_type == 'non_recyclable' and bin_instance.non_recyclable_fill_level < 50:
        #     return Response({'message': 'Cannot pickup at the moment.'}, status=status.HTTP_400_BAD_REQUEST)
        # Create a WasteHistory entry
        wasteHistory.objects.create(
            bin=bin_instance,
            quantity=0,  # This would be calculated
            points=0,  # This would be calculated
            status='pending',
            type=waste_type,
            user=request.user,
        )
        return Response({'message': 'Pickup request created successfully.'}, status=status.HTTP_201_CREATED)

class MonthlyRewardPointsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        # Logic to calculate reward points for each month (simplified example)
        points = wasteHistory.objects.filter(user_id=user_id).values('points')
        return Response({'points': points}, status=status.HTTP_200_OK)

class BinRewardPointsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        bin_id = request.query_params.get('bin_id')
        bin_instance = wasteBin.objects.get(id=bin_id)
        points = wasteBin.reward_points_sum_bin_count()
        return Response({'points': points}, status=status.HTTP_200_OK)