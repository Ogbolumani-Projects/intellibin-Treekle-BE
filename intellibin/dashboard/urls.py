from django.urls import path, include
from .views import *
urlpatterns = [
    path('dashboard/', DashBoardView.as_view())
]