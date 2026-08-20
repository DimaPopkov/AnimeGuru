from django.contrib.auth.signals import user_logged_in
from .models import UserActivityLog
from django.utils import timezone
from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_updated, social_account_added

def log_user_activity(sender, user, request, **kwargs):
    UserActivityLog.objects.get_or_create(
        user=user,
        date=timezone.now().date()
    )

user_logged_in.connect(log_user_activity)

@receiver([social_account_updated, social_account_added])
def update_discord_avatar_on_login(request, sociallogin, **kwargs):
    # Проверяем, что обновление пришло именно от Discord провайдера
    if sociallogin.account.provider == 'discord':
        # Вытаскиваем свежие JSON-данные, которые только что прислал Discord
        new_extra_data = sociallogin.account.extra_data
        
        # Получаем уже существующий объект аккаунта из базы данных
        social_account = sociallogin.account
        
        # Принудительно обновляем поле extra_data актуальной информацией
        social_account.extra_data = new_extra_data
        social_account.save()
        
        print(f"[AnimeGuru] Аватарка для {social_account.user.username} успешно обновлена из Discord!")