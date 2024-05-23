from django.urls import path
#from rest_framework_simplejwt.views import ( TokenRefreshView, TokenObtainPairView)
from .views import RegisterUser, LoginView

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login')
]