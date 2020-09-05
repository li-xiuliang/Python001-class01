from django.urls import path, re_path, register_converter
from . import views


urlpatterns = [
    path('', views.index),
    path('phone/', views.single_phone),
    path('author/', views.comments_author),
    path('time/', views.publish_time),
]