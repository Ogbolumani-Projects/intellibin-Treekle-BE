from django.urls import path
#from rest_framework_simplejwt.views import ( TokenRefreshView, TokenObtainPairView)
from .views import RegisterUser

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
]