from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import ValidationError, UniqueValidator
from django.contrib.auth.password_validation import validate_password
#from .models import CustomUserManager, UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

# class UserRegisterSerializer(serializers.ModelSerializer):
#     confirm_password = serializers.CharField(write_only= True)
#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(queryset=User.objects.all())]
#     )
#     password = serializers.CharField(
#         write_only=True, required=True, validators=[validate_password])

#     class Meta:
#         model = User
#         fields = ('email', 'password', 'confirm_password', 'phone_number', 'first_name', 'last_name', 'address')
#         extra_kwargs = { 'password': {'write_only': True},
#                          'confirm_password':{'write_only': True}
#         }
    
#     def validate(self, attrs):
#         if attrs['password'] != attrs['confirm_password']:
#             raise serializers.ValidationError(
#             {"password": "Password fields didn't match."})
#         try:
#             validate_password(attrs['password'])
#         except ValidationError as err:
#             raise serializers.ValidationError(
#             {"password": err.messages})
#         return attrs

#     def create(self, validated_data):
#         new_user = User.objects.create(
#             email = validated_data['email'],
#         )
#         new_profile = UserProfile.objects.create(user = new_user)
#         new_user.set_password(validated_data['password'])
#         new_user.save()

#         return new_user

# class UserLoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUserManager
#         fields = ('id','email', 'password')
