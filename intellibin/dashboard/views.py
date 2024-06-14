from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import viewsets
from .serializers import *
from django.http import Http404
from .models import *

from django.http.response import HttpResponse
# Create your views here.


class DashBoardView(APIView):

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
                'user': request.user.firstname,
                'total_reward_point': waste_bins[0].reward_points_sum_bin_count(),
                'waste_bins':waste_bin_list,
                'full_bins':waste_bins[0].full_bins(),
                'half_bins':waste_bins[0].half_bins(),
                'other_bin_levels':waste_bins[0].spacious_bins()

            }
        )
    
    def post(self, request):
        pass
