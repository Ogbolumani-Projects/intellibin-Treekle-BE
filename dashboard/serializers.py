from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from administration.utils import *

User = get_user_model()


class WasteBinSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), queryset=User.objects.all())
    full_bins = serializers.SerializerMethodField()
    spacious_bins = serializers.SerializerMethodField()
    half_bins = serializers.SerializerMethodField()
    bin_level_ = serializers.SerializerMethodField()
    weight_ = serializers.SerializerMethodField()
    temperature = serializers.FloatField()
    weight = serializers.FloatField() 
    bin_level  = serializers.FloatField()
    humidity = serializers.FloatField()

    class Meta:
        model = WasteBin
        fields = "__all__"
        extra_fields = ["full_bins", "spacious_bins", "half_bins", "user","temperature","weight"]
        exclude = ()


    def get_full_bins(self, obj):
        return obj.full_bins
    
    def get_half_bins (self, obj):
        print(obj)
        return obj.half_bins
    
    def get_spacious_bins(self, obj):
        return obj.spacious_bins
    
    def get_bin_level_(self, obj):
        return obj.bin_level
    
    def get_weight_(self, obj):
        return obj.weight
    
    def update(self, instance, validated_data):

        print(validated_data)
        
        instance.reward_points = validated_data.get("reward_points", instance.reward_points)
        instance.charge_status = validated_data.get("charge_status", instance.charge_status)
        instance.power_consumption = validated_data.get("power_consumption", instance.power_consumption)
        instance.charge_status = validated_data.get("charge_status", instance.charge_status)
        instance.battery_level = validated_data.get("battery_level", instance.battery_level)
        instance.battery_status = validated_data.get("battery_status", instance.battery_status)
        instance.location = validated_data.get("location", instance.location)
        instance.latitude = validated_data.get("latitude", instance.latitude)
        instance.longitude = validated_data.get("longitude", instance.longitude)
        instance.humidity = validated_data.get("humidity", instance.humidity)
        recy =  instance.compartments.filter(type_of_waste="RECYCLABLE")[0]
        recy.weight = validated_data.get("weight", recy.weight)
        update_bin(recy, validated_data)
        recy.save()
        instance.save()
        return instance
        
class RequestWasteBinSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), queryset=User.objects.all())

    class Meta:
        model = WasteBinRequest
        fields = ["user", "location", "latitude",
                  "longitude", "date_requested"]


class WastePickRequestSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(default = serializers.CurrentUserDefault(), queryset = User.objects.all())
    parent_bin = serializers.PrimaryKeyRelatedField(queryset=WasteBin.objects.all())

    class Meta:
        model  = WastePickUp
        fields = "__all__"

class DashboardParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BinCompartment 
        fields = '__all__'

class SaveDataSerializer(serializers.Serializer):
    pass

class SaveSensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveSensorData
        fields = [
            'bin_id',
            'date',
            'time',
            'waste_height',
            'temperature',
            'humidity',
            'weight',
            'batt_value',
            'latitude',
            'longitude',
            # 'weather_condition',
        ]