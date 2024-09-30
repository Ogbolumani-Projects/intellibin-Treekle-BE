from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *
from dj_rest_auth.urls import PasswordResetView, PasswordResetConfirmView, PasswordChangeView, LogoutView


urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegisterAPIView.as_view(), name='login'),
    path("resend_otp/", resend_otp_token, name='resend_otp'),
    path("confirm_otp/", confirm_otp, name='confirm_otp'),
    path("user_profile/", UserProfileAPIView.as_view(), name='user_profile'),
    path('change-password/', change_password, name='change_password'),
    path('password-reset/',
         include('django_rest_passwordreset.urls', namespace='password_reset'))
    # path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset-confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),


]
