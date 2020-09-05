'''
Author: your name
Date: 2020-08-22 19:10:28
LastEditTime: 2020-08-23 09:18:20
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /auth_learn/users/urls.py
'''
from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('index/', views.index),
    path('register/', views.register, name = 'register'),
]