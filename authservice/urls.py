from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *



urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',UserRegisterAPIView.as_view(), name='login'),
    path("resend_otp/", resend_otp_token, name='resend_otp'),
    path("confirm_otp/", confirm_otp, name='confirm_otp'),
    path("user_profile/", UserProfileAPIView.as_view(), name='user_profile'),
    path('change-password/', PasswordChangeAPIView.as_view(), name='change_password'),
    path('password-reset/', PasswordResetAPIView.as_view(), name='password_reset'),
    path('password-reset-confirm/', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    #path('user/password/reset/', PasswordResetAPIView.as_view(), name='rest_password_reset'),
    # path('user/password/reset/confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),
    #      name='password_reset_confirm'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done')
]