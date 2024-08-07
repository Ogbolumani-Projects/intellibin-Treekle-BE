from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("WasteBin", WasteBinPickupView, basename="wastebin pickup")
router.register("dashboard", DashViewset, basename="dashboard")
router.register("bin-request", WasteBinRequest, basename="bin-request")
urlpatterns = [
    
]+router.urls

# urlpatterns = [
#     path('dashboard/', DashBoardView.as_view()),
#     path('request_pickup/', WasteBinPickupView.as_view()),
#     path('request-bin/', RequestBinView.as_view(), name='request-bin'),
#     path('bins/', wasteBinListView.as_view(), name='bin-list'),
#     path('bins/<int:pk>/', BinDetailView.as_view(), name='bin-detail'),
#     path('request-pickup/', RequestPickupView.as_view(), name='request-pickup'),
#     path('monthly-reward-points/', MonthlyRewardPointsView.as_view(), name='monthly-reward-points'),
#     path('bin-reward-points/', BinRewardPointsView.as_view(), name='bin-reward-points'),

# ]