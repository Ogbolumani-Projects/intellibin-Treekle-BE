
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'admin_analytics_api'
urlpatterns = [
    path('user', views.user_analytics, name='user_analytics'),
]
