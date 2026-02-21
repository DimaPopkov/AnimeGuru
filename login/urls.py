from django.contrib import admin
from django.urls import path, include

from . import views
from main.views import courent_theme

urlpatterns = [
    path('', views.Login, name="Login"),
    path('create_user/', views.create_user, name="create_user"),
    path('theme/get/', courent_theme), 
    path('theme/set/', views.save_theme),
]
