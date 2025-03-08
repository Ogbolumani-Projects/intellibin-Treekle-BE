from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Bin, WasteData, WeatherData, CustomerProfile, EmployeeProfile, AdminProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class BinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bin
        fields = '__all__'

class WasteDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteData
        fields = '__all__'

class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = '__all__'

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = CustomerProfile
        fields = '__all__'

class EmployeeProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = EmployeeProfile
        fields = '__all__'

class AdminProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = AdminProfile
        fields = '__all__'