from rest_framework import serializers
from authservice.models import CustomUser, UserProfile
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate


class AdminRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("email", "password", "confirm_password",
                  "first_name", "last_name", "middle_name", "phone_number", "address")
        extra_kwargs = {'password': {'write_only': True},
                        "confirm_password": {'write_only': True}}

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
            email=validated_data['email'],
            address=validated_data['address'],
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            is_admin=True
        )
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        label='email'
    )
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        if email and password:
            user = authenticate(
                username=email, password=password, request=self.context.get(
                    'request')
            )

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
            elif not user.is_admin:
                msg = 'Sorry! Only admins are allowed to login.'
                raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
