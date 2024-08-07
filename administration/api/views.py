from django.forms import ValidationError
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from administration.api.serializers import AdminRegisterSerializer, AdminLoginSerializer
from authservice.models import CustomUser
from authservice.utils import send_mail_to_user
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

# Create your views here.


class AdminRegisterAPIView(APIView):
    queryset = CustomUser
    serializer_class = AdminRegisterSerializer

    def post(self, request, *args, **kargs):
        serializer = AdminRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            send_otp = send_mail_to_user(serializer.data['email'])

            response = {
                'success': True,
                'user': serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        raise ValidationError(
            serializer.errors, code=status.HTTP_406_NOT_ACCEPTABLE)


class AdminLoginAPIView(APIView):
    queryset = CustomUser
    serializer_class = AdminLoginSerializer

    def post(self, request, *args, **kargs):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                "email": {
                    "detail": "User Does not exist!"
                }
            }
            if CustomUser.objects.filter(email=request.data['email']).exists():
                user = CustomUser.objects.get(email=request.data['email'])
                refresh = RefreshToken.for_user(user)

                response = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
