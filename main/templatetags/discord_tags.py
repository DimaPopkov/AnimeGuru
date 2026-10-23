import requests
import urllib3
from django import template
from django.core.cache import cache
from allauth.socialaccount.models import SocialToken

register = template.Library()

# Отключаем предупреждения об отсутствии SSL-валидации на PythonAnywhere
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@register.filter
def get_fresh_discord_avatar(account):
    """
    Кастомный фильтр шаблона. Берет личный access_token пользователя
    и раз в час проверяет актуальный аватар через OAuth2 напрямую у Discord.
    """
    if account.provider != 'discord':
        return account.get_avatar_url()

    discord_id = account.uid
    cache_key = f"discord_oauth_avatar_{discord_id}"
    
    # 1. Возвращаем из кэша, если запрос уже делался в течение последнего часа
    cached_url = cache.get(cache_key)
    if cached_url:
        return cached_url

    # Запасной вариант (старая ссылка из extra_data базы данных)
    fallback_url = account.get_avatar_url() or "/static/img/null_avatar.png"

    # 2. Ищем сохраненный access_token этого аккаунта в БД
    token_obj = SocialToken.objects.filter(account=account).first()
    if not token_obj or not token_obj.token:
        return fallback_url

    # 3. Настройка прокси под бесплатный тариф PythonAnywhere
    proxies = {
        "http": "http://proxy.server:3128",
        "https": "http://proxy.server:3128",
    }
    
    # Делаем запрос от имени ПОЛЬЗОВАТЕЛЯ (Bearer token) на эндпоинт @me
    headers = {"Authorization": f"Bearer {token_obj.token}"}
    url = "https://discord.com"
    
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=4, verify=False)
        
        if response.status_code == 200:
            data = response.json()
            avatar_hash = data.get("avatar")
            
            if avatar_hash:
                fresh_url = f"https://discordapp.com{discord_id}/{avatar_hash}.png"
            else:
                fresh_url = "/static/img/null_avatar.png"
            
            # Кэшируем ровно на 1 час (3600 секунд)
            cache.set(cache_key, fresh_url, 3600)
            return fresh_url
            
        elif response.status_code == 401:
            # Если токен окончательно протух (например, прошло больше недели с последнего логина),
            # отдаем старую ссылку, пока пользователь не переразлогинится
            return fallback_url
            
    except requests.RequestException:
        pass
        
    return fallback_url