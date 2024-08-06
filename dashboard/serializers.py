from rest_framework import serializers
from .models import *

class WastePickRequestSerializer(serializers.Serializer):
    type_of_waste = serializers.CharField()

class wasteBinSerializer(serializers.ModelSerializer):
    class Meta:
        model = wasteBin
        fields = ['id', 'is_active', 'location', 'battery_status', 'temperature', 'bin_level', 'user']

class WasteHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = wasteHistory
        fields = ['id', 'bin', 'date_time', 'quantity', 'points', 'status', 'type', 'user']