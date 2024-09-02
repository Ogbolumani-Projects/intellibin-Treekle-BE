from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers
from authservice.models import *
from dashboard.models import *
from .utils import *

class UserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = "__all__"

class CompartmentSerializer(Serializer):
    comp_type = serializers.JSONField(required=False)

class AdminWasteBinSerializer(ModelSerializer):
    id = serializers.IntegerField(required = False)
    compartments = CompartmentSerializer(required=False)
    full_bins = serializers.SerializerMethodField()
    spacious_bins = serializers.SerializerMethodField()
    half_bins = serializers.SerializerMethodField()
    bin_level = serializers.SerializerMethodField()
    weight = serializers.SerializerMethodField()
    
    class Meta:
        model = WasteBin
        fields = "__all__"
        extra_fields = ("compartments")
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
    
    def create(self, validated_data):
        Bin = WasteBin.objects.create(
                            **validated_data
                        )

        comp_1 = BinCompartment.objects.create(
                            parent_bin = Bin, type_of_waste = "RECYCLABLE"
                        )

        comp_2 = BinCompartment.objects.create(
                            parent_bin = Bin, type_of_waste = "NON_RECYCLABLE"
                        )
        
        data =list( WasteBin.objects.filter(id=Bin.id).prefetch_related("compartments").values())
        
        data[0]['compartments'] = Bin.compartments.values()
        print(data[0])

        # print(data[0]['compartments'])
        return data



    def update(self, instance, validated_data):

        compartments  = validated_data.pop("compartments", None) 
        print(compartments)
        instance.user = validated_data.get("user", instance.user)
        instance.reward_points = validated_data.get("reward_points", instance.reward_points)
        instance.charge_status = validated_data.get("charge_status", instance.charge_status)
        instance.power_consumption = validated_data.get("power_consumption", instance.power_consumption)
        instance.charge_status = validated_data.get("charge_status", instance.charge_status)
        instance.battery_level = validated_data.get("battery_level", instance.battery_level)
        instance.battery_status = validated_data.get("battery_status", instance.battery_status)
        instance.location = validated_data.get("location", instance.location)
        instance.latitude = validated_data.get("latitude", instance.latitude)
        instance.longitude = validated_data.get("longitude", instance.longitude)

        instance.save()

        if compartments:
            
            if "recyclable" in compartments["comp_type"].keys():
                
                recy_ = instance.compartments.filter(type_of_waste="RECYCLABLE")[0]
                print(recy_.weight)
                update_bin(compartments=recy_, data = compartments["comp_type"]['recyclable'] )
                

            if "non_recyclable" in compartments["comp_type"].keys():
                non_recy_ = instance.compartments.filter(type_of_waste="NON_RECYCLABLE")
                update_bin(non_recy_, compartments["comp_type"]['non_recyclable'])
            
        
        return instance

    
    


# Create your tests here.


class WasteRequestSerializer(ModelSerializer):
    class Meta:
        model  = WasteBinRequest
        fields = "__all__"


    def update(self, instance, validated_data):
        prev_pending = instance.pending
        prev_approved = instance.approved

        instance.location = validated_data.get("location", instance.location)
        instance.longitude = validated_data.get("longitude", instance.longitude)
        instance.latitude = validated_data.get("latitude", instance.latitude)
        instance.pending = validated_data.get("pending", instance.pending)
        instance.approved = validated_data.get("approved", instance.approved)
        
        if prev_pending and not instance.pending:

                if prev_approved:
                     
                    return instance
                else:
                    if instance.approved:

                        instance.approved = validated_data.get("approved", instance.approved)

                        Bin = WasteBin.objects.create(
                            user=instance.user, location = instance.location, latitude = instance.latitude, longitude=instance.longitude
                        )

                        comp_1 = BinCompartment.objects.create(
                            parent_bin = Bin, type_of_waste = "RECYCLABLE"
                        )

                        comp_2 = BinCompartment.objects.create(
                            parent_bin = Bin, type_of_waste = "NON_RECYCLABLE"
                        )
        
        return instance

    


    



