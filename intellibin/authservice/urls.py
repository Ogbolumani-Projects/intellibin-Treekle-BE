from django.urls import path
#from .import views
from .views import LoginView, RegisterView, ResendOTPView, VerifyEmailView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/<str:username>/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
    # path("register/", views.signup, name="register"), 
    # path("verify-email/<slug:username>", views.verify_email, name="verify-email"),
    # path("resend-otp/", views.resend_otp, name="resend-otp"),
    # path("login/", views.signin, name="signin"),
    #path('test-email/', TestEmailView.as_view(), name='test-email')
]