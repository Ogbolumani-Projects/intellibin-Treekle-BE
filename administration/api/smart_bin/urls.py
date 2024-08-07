
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'smart_bin_api'
urlpatterns = [
    path('', views.AllWasteBinsView.as_view(), name='get_all_smart_bins'),
    path('<int:id>', views.smart_bin_detail, name='smart_bin_detail'),
    path('activate/<int:id>', views.activate_smart_bin, name='activate_smart_bin'),
    path('deactivate/<int:id>', views.deactivate_smart_bin,
         name='deactivate_smart_bin'),
    path('create/', views.create_smart_bin, name='create_smart_bin'),
]
