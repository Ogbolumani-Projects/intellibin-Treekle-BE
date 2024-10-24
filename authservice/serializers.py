from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .backends import EmailPhoneNumberBackend
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from dj_rest_auth.serializers import PasswordResetSerializer, PasswordResetConfirmSerializer, PasswordChangeSerializer
from .utils import *

import secrets
import time
import random

class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser  
        fields=("email", "password", "confirm_password", "phone_number", "first_name", "last_name","address")
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
            phone_number = validated_data['phone_number'], 
            first_name= validated_data['first_name'], 
            last_name= validated_data['last_name'], 
            address = validated_data['address'], 
            verified=False
        )
        new_profile = UserProfile.objects.create(user=new_user)
        new_user.set_password(validated_data['password'])
        new_user.save()
    
        #sending otp to the user
        send_otp = send_mail_to_user({new_user.email})
        return new_user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label='username or email'
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
            print('user:', user)
            print('user verify:', user.verified)
            
        #to check if the user is verified or not
            if not user.verified:
                print('check')
                raise serializers.ValidationError(
                    {"detail": "User is not verified, please verify your account before logging in"}, code = 'authorization'        
                )

        attrs['user'] = user
        return attrs


class ConfirmOTPSerializer(serializers.Serializer):
    otp = serializers.CharField()
    email = serializers.EmailField()


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UpdateUserProfileSerializer(serializers.ModelSerializer):    
    class Meta:
        model = CustomUser
        fields = "__all__"

    def validate(self, attrs):
        if 'phone_number' in attrs.keys() or 'email' in attrs.keys():
            raise serializers.ValidationError(
            {"error": "You cannot update your phone number or email address "})
        return attrs 


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()    

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()


class CustomUserSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


     