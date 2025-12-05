import json
from django.urls import path
from unfold.admin import ModelAdmin
from django.views.generic import TemplateView
from unfold.views import UnfoldModelAdminViewMixin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin

from django.db.models import Count
from django.contrib.auth import get_user_model
from django.db.models.functions import TruncDay

from datetime import timedelta

from django.contrib import admin
from .models import Product, Category, Tags, Pics, Album_Pics, Status, Weblinks, Voice_maker, Characters, Comments, CommentAction, UserActivity

# Register your models here.

admin.site.index_title = 'Dashboard'

class DashboardView(UnfoldModelAdminViewMixin, TemplateView):
    title = "Dashboard"
    permission_required = ()
    template_name = "admin/index.html"

class DashboardAdmin(ModelAdmin):
    def get_urls(self):
        return super().get_urls() + [
            path(
                "index", 
                DashboardView.as_view(model_admin=self),
                name="index"
            ),
        ]

User = get_user_model() 

def dashboard_callback(request, context):
    now = timezone.now()
    seven_days_ago = now - timezone.timedelta(days=7)

    # --- KPI Section ---
    # 1. Total Active Users (Last 7 days)
    # Используем стандартную модель User
    active_users_last_7_days = User.objects.filter(last_login__gte=seven_days_ago).count()

    # 2. Additional KPI (Example: Total registered users)
    total_registered_users = User.objects.count()

    # --- Chart Data Section ---

    # DAU Chart Data (Daily Active Users)
    # Получаем данные за последние 7 дней, группируем по дням
    # TruncDay требует, чтобы поле было DateTimeField. last_login - это DateTimeField.
    dau_data = User.objects.filter(last_login__gte=seven_days_ago).annotate(
        date=TruncDay('last_login')
    ).values('date').annotate(count=Count('id')).order_by('date')

    # Создаем полный список дат за последние 7 дней (включая сегодня)
    full_date_range = [(now - timezone.timedelta(days=i)) for i in range(6, -1, -1)]
    final_dates = [d.strftime('%Y-%m-%d') for d in full_date_range]
    final_dau_values = [0] * len(final_dates)

    # Сопоставляем полученные данные с полным диапазоном дат
    # Создаем словарь для быстрого поиска данных по дате
    dau_dict = {entry['date'].strftime('%Y-%m-%d'): entry['count'] for entry in dau_data}

    for i, date_str in enumerate(final_dates):
        final_dau_values[i] = dau_dict.get(date_str, 0) # Получаем значение или 0, если данных нет

    dauChartData = json.dumps({
        'datasets': [
            {'data': final_dau_values,
             'borderColor': 'rgb(200, 200, 200)',
             'label': 'Daily Active Users'
            }
        ],
        'labels': final_dates
    })

    # Optional: Another chart for user registration dates
    # This chart will show how many users registered each day
    registration_data = User.objects.annotate(
        date=TruncDay('date_joined')
    ).values('date').annotate(count=Count('id')).order_by('date')

    final_registration_values = [0] * len(final_dates)
    registration_dict = {entry['date'].strftime('%Y-%m-%d'): entry['count'] for entry in registration_data}

    for i, date_str in enumerate(final_dates):
        final_registration_values[i] = registration_dict.get(date_str, 0)

    registrationChartData = json.dumps({
        'datasets': [
            {'data': final_registration_values,
             'borderColor': 'rgb(200, 200, 200)',
             'label': 'New Registrations'
            }
        ],
        'labels': final_dates
    })

    context.update(
        {
            "kpis": [
                {
                    "title": "Total Active Users (Last 7 days)",
                    "metric": active_users_last_7_days,
                },
                {
                    "title": "Total Registered Users",
                    "metric": total_registered_users,
                },
            ],
            "dauChartData": dauChartData,
            "registrationChartData": registrationChartData,
        }
    )
    return context


admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_login_date', 'login_count_today')
    readonly_fields = ('user', 'last_login_date', 'login_count_today') # Сделаем поля только для чтения, так как они обновляются сигналами

    def has_add_permission(self, request):
        return False # Запретим ручное добавление записей

    def has_delete_permission(self, request, obj=None):
        return False # Запретим удаление записей
    

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    pass

@admin.register(Tags)
class TagsAdmin(ModelAdmin):
    pass

@admin.register(Pics)
class PicsAdmin(ModelAdmin):
    pass

@admin.register(Album_Pics)
class Album_PicsAdmin(ModelAdmin):
    pass

@admin.register(Status)
class StatusAdmin(ModelAdmin):
    pass

@admin.register(Weblinks)
class WeblinksAdmin(ModelAdmin):
    pass

@admin.register(Voice_maker)
class Voice_makerAdmin(ModelAdmin):
    pass

@admin.register(Characters)
class CharactersAdmin(ModelAdmin):
    pass

@admin.register(Comments)
class CommentsAdmin(ModelAdmin):
    pass

@admin.register(CommentAction)
class CommentActionAdmin(ModelAdmin):
    pass