
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'pickup_request_api'
urlpatterns = [
    path('pending/', views.PendingPickupRequestsView.as_view(),
         name='get_pending_pickup_requests'),
    path('confirmed/', views.ConfirmedPickupRequestsView.as_view(),
         name='get_confirmed_pickup_requests'),
    path('fulfilled/', views.FulfilledPickupRequestsView.as_view(),
         name='get_fulfilled_pickup_requests'),
    path('update-status/<int:id>', views.update_pickup_status_request,
         name='update_pickup_status_request'),
]
