"""
URL configuration for intellibin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView, LogoutView
from django.contrib.auth import views as auth_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

urlpatterns = [
    path('admin/', admin.site.urls),

    # admin urls
    path('api/v1/admin/', include('administration.api.urls')),
    path('api/v1/admin/smartbins/', include('administration.api.smart_bin.urls')),
    path('api/v1/admin/pick-up-request/',
         include('administration.api.requests.urls')),
    path('api/v1/admin/analytics/', include('administration.api.analytics.urls')),

    path('api/v1/users/', include('authservice.urls')),
    path('api/v1/wastebin/', include('dashboard.urls')),
    path('admin/', include('administration.urls')),
    path('payments/', include("payments.urls")),

    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
