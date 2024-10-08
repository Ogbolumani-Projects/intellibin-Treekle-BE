from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *
from dj_rest_auth.urls import PasswordResetView, PasswordResetConfirmView, PasswordChangeView, LogoutView


urlpatterns = [
    path('register/', AdminRegisterAPIView.as_view(), name='register'),
    path('login/', AdminLoginAPIView.as_view(), name='login'),
]
