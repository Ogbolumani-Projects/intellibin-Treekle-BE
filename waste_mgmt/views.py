from django.shortcuts import render

# Create your views here.
import uuid
from .models import Bin, WasteData
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Point
from .serializers import BinSerializer, WasteDataSerializer

class BinViewSet(viewsets.ModelViewSet):
    queryset = Bin.objects.all()
    serializer_class = BinSerializer

class WasteDataViewSet(viewsets.ModelViewSet):
    queryset = WasteData.objects.all()
    serializer_class = WasteDataSerializer

@api_view(['GET'])
def recieve_iot_data(request):
    try:
        # Validate required parameters
        params = request.query_params
        required_fields = [
            'bin_id', 'waste_height', 'temperature', 
            'humidity', 'weight', 'batt_value',
            'latitude', 'longitude'
        ]
        
        # Check for missing fields
        missing = [field for field in required_fields if field not in params]
        if missing:
            return Response(
                {"error": f"Missing parameters: {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Convert parameters to appropriate types
        try:
            bin_id = uuid.UUID(params['bin_id'])
            waste_height = float(params['waste_height'])
            temperature = float(params['temperature'])
            humidity = float(params['humidity'])
            weight = float(params['weight'])
            batt_value = float(params['batt_value'])
            latitude = float(params['latitude'])
            longitude = float(params['longitude'])
        except ValueError as e:
            return Response(
                {"error": f"Invalid parameter value: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get bin and update location
        bin = Bin.objects.get(bin_id=bin_id)
        bin.location = Point(longitude, latitude, srid=4326)
        bin.current_level = waste_height
        bin.save()

        # Create waste data record
        WasteData.objects.create(
            bin=bin,
            weight=weight,
            fill_level=waste_height,
            temperature=temperature,
            humidity=humidity,
            battery_level=batt_value
        )

        return Response({
            "status": "success",
            "bin_id": str(bin_id),
            "current_level": waste_height
        }, status=status.HTTP_201_CREATED)

    except Bin.DoesNotExist:
        return Response(
            {"error": "Bin not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    except KeyError as e:
        return Response(
            {"error": f"Missing parameter: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        # Log the unexpected error for debugging
        print(f"Unexpected error: {str(e)}")
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
