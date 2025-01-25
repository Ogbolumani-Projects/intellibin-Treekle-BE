from rest_framework import serializers
from .models import Bin, WasteData

class BinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bin
        fields = '__all__'

class WasteDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteData
        fields = '__all__'