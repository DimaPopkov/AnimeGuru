import json
from django.urls import path
from unfold.admin import ModelAdmin
from django.views.generic import TemplateView
from unfold.views import UnfoldModelAdminViewMixin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin

from django.db.models import Count
from django.contrib.auth import get_user_model
from django.db.models.functions import TruncDay

from datetime import timedelta

from django.contrib import admin
from .models import Posts, PostsAction

@admin.register(Posts)
class PostsAdmin(ModelAdmin):
    pass

@admin.register(PostsAction)
class PostsActionAdmin(ModelAdmin):
    pass