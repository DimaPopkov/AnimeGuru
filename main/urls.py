from django.contrib import admin
from django.urls import path, include, re_path, reverse_lazy
from django.contrib.auth.views import LogoutView
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.main, name="main"),
    path('admin/', admin.site.urls),
    path('about/', views.about, name="about"),
    path('theme/get/', views.courent_theme), 
    path('theme/set/', views.save_theme),
    path('create/', views.create, name="create"),
    path('filtered-items/', views.filter, name='filtered-items'),
    path('card/<str:product_name>/favourites_add/', views.favourites_add, name='favourites_add'),
    path('comment/<int:comment_id>/state/', views.update_comment_state, name='comment'),
    path('add_comments/<str:product_name>/', views.add_comments, name='add_comments'),
    path('edit_comments/<str:product_name>/', views.edit_comments, name='edit_comments'),
    path('delete_comments/<str:product_name>/<str:id>/', views.delete_comments, name='delete_comments'),
    path('card/<str:product_name>/', views.card, name="card"),
    path('login/', include('login.urls')),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('main')), name='logout'),
    path('user/', views.profile, name='profile'),
    path('user/change-avatar', views.profile_change_avatar, name='profile_change_avatar'),
    path('AI/chat', views.AIchat, name='AIchat'),
    path('AI/history', views.AIhistory, name='AIhistory'),
    path('posts/', include('posts.urls'), name='posts'),
    path('copyright/', views.copyright, name='copyright'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)