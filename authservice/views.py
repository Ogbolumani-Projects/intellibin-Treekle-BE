from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from .models import *
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from dj_rest_auth.views import ( PasswordResetView, PasswordResetConfirmView, PasswordChangeView, LogoutView)


from .serializers import *

from .utils import *

class UserRegisterAPIView(APIView):
    queryset = CustomUser
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kargs):
        serializer = UserRegisterSerializer(data=request.data)
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
    
class UserLoginAPIView(APIView):
    queryset = CustomUser
    serializer_class = UserLoginSerializer
    def post(self, request, *args, **kargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            response = {
                "username": {
                    "detail": "User Does not exist!"
                }
            }
            if CustomUser.objects.filter(username=request.data['email']).exists():
                user = CustomUser.objects.get(username=request.data['email'])
                
                response = {
                    'success': True,
                    'username': user.username,
                    'email': user.email,
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def resend_otp_token(request, *args, **kwargs):

    serializers = ResendOTPSerializer(data=request.data)

    if serializers.is_valid():
        get_user = CustomUser.objects.filter(email=serializers.data['email']).exists() # true or false

        if get_user:
            get_user = CustomUser.objects.get(email=serializers.data['email']) 
            send_email_with_otp = send_mail_to_user(get_user.email)
            return Response("OTP has been sent")
        
        return Response("wrong email")
    return Response(serializers.errors)


@api_view(["POST"])
def confirm_otp(request):

    serializer = ConfirmOTPSerializer(data = request.data)

    if serializer.is_valid():

        confirm_otp_code = totp.verify(serializer.data['otp'])

        if confirm_otp_code:
            verified_user = CustomUser.objects.get(email=serializer.data['email'])
            verified_user.verified = True
            verified_user.save()

    
            return Response("You are now verified")
        else:
            return Response(
                "Otp expired or incorrect"
            )
    return Response(serializer.errors)

class UserProfileAPIView(APIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()
    def get(self, request):
        print(request.user)
        user = CustomUser.objects.get(email=request.user.email)

        return Response(
            {
            'email':user.email,
            'full_name': user.full_name,
            'phone_number': user.phone_number
            }
        )
    
    def put(self,request):
        get_user = CustomUser.objects.get(id=request.user.id)
        serializers = UpdateUserProfileSerializer(get_user, data= request.data, partial=True)

        if serializers.is_valid():
   
            serializers.save()

            return Response(
                serializers.data
            )
        return Response(
            serializers.errors
        ) 

class PasswordChangeAPIView(PasswordChangeView):
    """
    View for changing password.
    Inherits from dj_rest_auth's PasswordChangeView.
    """

# class PasswordResetAPIView(PasswordResetView):
#     """
#     View for initiating password reset process.
#     Inherits from dj_rest_auth's PasswordResetView.
#     """

# class PasswordResetConfirmAPIView(PasswordResetConfirmView):
#     """
#     View for confirming password reset process.
#     Inherits from dj_rest_auth's PasswordResetConfirmView.
#     """
    
class LogoutAPIView(LogoutView):
    """
    View for user logout.
    Inherits from dj_rest_auth's LogoutView.
    """

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def change_password(request):
#     if request.method == 'POST':
#         serializer = ChangePasswordSerializer(data=request.data)
#         if serializer.is_valid():
#             user = request.user
#             if user.check_password(serializer.data.get('old_password')):
#                 user.set_password(serializer.data.get('new_password'))
#                 user.save()
#                 update_session_auth_hash(request, user)  # To update session after password change
#                 return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
#             return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserRegisterSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)