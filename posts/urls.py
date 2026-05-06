from django.conf.urls.i18n import i18n_patterns

from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = (
    path('', views.posts, name="posts"),
    path('post/<str:post_id>/', views.card, name="post"),
    path('create/', views.create_form, name="create"),
    path('create/confirm', views.create, name="confirm"),
    path('post/<str:post_id>/update_state', views.update_post_state, name="update_post_state"),
)