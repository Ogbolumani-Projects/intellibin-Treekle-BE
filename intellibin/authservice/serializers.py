from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
import secrets

import time
import random

class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser  
        fields=("email", "password", "confirm_password")
        extra_kwargs = {'password': {'write_only': True}, # key word argument
                        "confirm_password":{'write_only':True}}
        
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
            {"password": "Password fields didn't match."})
       
        try:
            validate_password(attrs['password'])
        except ValidationError as err:
            raise serializers.ValidationError(
            {"password": err.messages})
        return attrs
    def create(self, validated_data):
        
        new_user = CustomUser.objects.create(
            email = validated_data['email'],
        )
        new_profile = UserProfile.objects.create(user=new_user)
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label='username or password'
    )
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']


        if username and password:
            user = authenticate(
                username=username, password=password,request=self.context.get('request')
            )

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs



class ConfirmOTPSerializer(serializers.Serializer):

    otp = serializers.CharField()
    email = serializers.EmailField()


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()