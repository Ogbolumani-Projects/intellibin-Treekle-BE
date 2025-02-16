# waste_mgmt/serializers.py
from rest_framework import serializers
# from djangorestframework import serializers
from .models import Bin, WasteData

class BinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bin
        fields = ['bin_id', 'location', 'capacity', 'current_level', 'batt_value', 'latitude', 'longitude', 'temperature', 'waste_height', 'humidity']

class WasteDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteData
        fields = ['timestamp', 'weight', 'fill_level', 'temperature', 'bin']
