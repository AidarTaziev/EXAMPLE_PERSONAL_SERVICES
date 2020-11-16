from django.urls import path
from tracking_maps import views

urlpatterns = [
    path('nomenclature', views.get_nomenclature),
    path('data', views.get_tracking_map_data),
]
