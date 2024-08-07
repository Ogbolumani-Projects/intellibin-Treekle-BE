from rest_framework.serializers import Serializer, ModelSerializer
from authservice.models import *
from dashboard.models import *

class UserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = "__all__"




# Create your tests here.


class WasteRequestSerialzier(ModelSerializer):

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
                            parent_bin = Bin, type_of_waste = "NON-RECYCLABLE"
                        )
        
        return instance