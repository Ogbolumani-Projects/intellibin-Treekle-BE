from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from authservice.serializers import CustomUserSerializer

User = get_user_model()


class WasteBinSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer(required=False)
    full_bins = serializers.SerializerMethodField()
    spacious_bins = serializers.SerializerMethodField()
    half_bins = serializers.SerializerMethodField()

    class Meta:
        model = WasteBin
        fields = "__all__"

    def full_bins(self, obj):
        return obj.full_bins

    def half_bins(self, obj):
        return obj.half_bins

    def spacious_bins(self, obj):
        return obj.spacious_bins


class RequestWasteBinSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), queryset=User.objects.all())

    class Meta:
        model = WasteBinRequest
        fields = ["user", "location", "latitude",
                  "longitude", "date_requested"]


class WastePickRequestSerializer(serializers.ModelSerializer):

    user = CustomUserSerializer(required=False)
    Bin = WasteBinSerializer()

    class Meta:
        model = WastePickUp
        fields = ["user", "Bin"]


# class WastePickRequestSerializer(serializers.Serializer):
#     type_of_waste = serializers.CharField()

# class wasteBinSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = wasteBin
#         fields = ['id', 'is_active', 'location', 'battery_status', 'temperature', 'bin_level', 'user']

# class WasteHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = wasteHistory
#         fields = ['id', 'bin', 'date_time', 'quantity', 'points', 'status', 'type', 'user']
