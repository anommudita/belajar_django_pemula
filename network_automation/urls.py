from django.urls import path
from . import views

urlpatterns = [

    path('', views.devices, name="devices"),


    # tambah devices
    path('tambah-devices/', views.tambah_device, name="tambah-devices"),

    # edit devices
    path('edit-device/<str:id_device>', views.edit_device, name="edit-device"),

    # delete devices
    path('delete-device/<str:id_device>', views.delete_device, name="delete-device"),

    path('config/', views.configure, name="config"),


]