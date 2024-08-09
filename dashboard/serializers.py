from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class WasteBinSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(default = serializers.CurrentUserDefault(), queryset=User.objects.all())
    full_bins = serializers.SerializerMethodField()
    spacious_bins = serializers.SerializerMethodField()
    half_bins = serializers.SerializerMethodField()
    bin_level = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    class Meta:
        model  = WasteBin
        fields = "__all__"

        extra_fields = ["full_bins", "spacious_bins", "half_bins"]
        exclude = ()



    def get_full_bins(self, obj):
        return obj.full_bins
    
    def get_half_bins (self, obj):
        print(obj)
        return obj.half_bins
    
    def get_spacious_bins(self, obj):
        return obj.spacious_bins
    
    def get_bin_level(self, obj):
        return obj.bin_level
    
    def get_weight(self, obj):
        return obj.weight
    

class RequestWasteBinSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(default = serializers.CurrentUserDefault(), queryset=User.objects.all())
    class Meta:
        model = WasteBinRequest
        fields = ["user", "location", "latitude", "longitude","date_requested"]

class WastePickRequestSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(default = serializers.CurrentUserDefault(), queryset = User.objects.all())
    parent_bin = WasteBinSerializer()

    class Meta:
        model  = WastePickUp
        fields = "__all__"