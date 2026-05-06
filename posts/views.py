from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.apps import apps
from django.db import models
from django.db.models import OuterRef, Subquery, FileField, F
from django.core.cache import cache

import base64
from django.core.files.base import ContentFile

from django.contrib.auth.models import User
from django.contrib import messages

from .models import Posts, PostsAction
import re, json, requests, Levenshtein

# Create your views here.
def posts(request):
    allPosts = list(Posts.objects.all())
    allPosts_state = PostsAction.objects.filter(user=request.user)

    for post in allPosts:
        post.net_likes = post.like_count - post.dislike_count
        post.my_state = 0

        for action in allPosts_state:
            if action.post_id == post.id: 
                if action.action_type == "like":
                    post.my_state = 2
                elif action.action_type == "dislike":
                    post.my_state = 1
                break

    new_posts = sorted(allPosts, key=lambda x: x.id, reverse=True)[:5]
    popular_posts = sorted(allPosts, key=lambda x: (x.net_likes, x.id), reverse=True)[:5]

    data = {
        'title': 'Лента публикаций',
        'new_posts' : new_posts,
        'posts': allPosts,
        'popular_posts': popular_posts,
    }

    return render(request, 'posts/main.html', data)

def card(request, post_id):
    post = get_object_or_404(Posts, id=post_id)

    data = {
        'title': post.title,
    }
        
    return render(request, 'posts/post.html', data)

def update_post_state(request, post_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)
    
    try:
        action = request.POST.get("action_ty")
        # Получаем комментарий один раз (без аннотации пока)
        post = get_object_or_404(Posts, id=post_id)
        
        # Получаем или создаем действие пользователя
        existing_action, created = PostsAction.objects.get_or_create(
            user=request.user, 
            post=post,
            defaults={'action_type': 'none'}
        )

        old_type = existing_action.action_type
        new_type = action # 'like' или 'dislike'

        if action == "like":
            if old_type == "like":
                # Отмена лайка
                existing_action.action_type = "none"
                post.like_count = F('like_count') - 1
            elif old_type == "dislike":
                # Переключение с дизлайка на лайк
                existing_action.action_type = "like"
                post.dislike_count = F('dislike_count') - 1
                post.like_count = F('like_count') + 1
            else:
                # Новый лайк
                existing_action.action_type = "like"
                post.like_count = F('like_count') + 1

        elif action == "dislike":
            if old_type == "dislike":
                # Отмена дизлайка
                existing_action.action_type = "none"
                post.dislike_count = F('dislike_count') - 1
            elif old_type == "like":
                # Переключение с лайка на дизлайк
                existing_action.action_type = "dislike"
                post.like_count = F('like_count') - 1
                post.dislike_count = F('dislike_count') + 1
            else:
                # Новый дизлайк
                existing_action.action_type = "dislike"
                post.dislike_count = F('dislike_count') + 1

        # Сохраняем изменения в базе
        existing_action.save()
        post.save()

        # Теперь ОДИН РАЗ обновляем объект, чтобы получить актуальные числа и net_likes
        post.refresh_from_db()
        current_net_likes = post.like_count - post.dislike_count

        return JsonResponse({
            'status': 'success',
            'net_likes': current_net_likes,
            'existing_action': existing_action.action_type
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
def create_form(request):
    data = {
        'title': "Создание публикации",
    }
    return render(request, 'posts/create.html', data)

def create(request):
    error_message = None
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        media_raw = request.POST.get('cropped_data')

        print("--- НОВЫЙ ЗАПРОС ---")
        print(f"Title: {request.POST.get('title')}")
        print(f"Text length: {len(request.POST.get('text', ''))}")
        print(f"Media length: {len(request.POST.get('cropped_data', ''))}")

        if not title:
            error_message = "Вы не ввели заголовок"
        elif not text:
            error_message = "Поле текста не может быть пустым"
        elif not media_raw:
            error_message = "Забыли загрузить обложку"
        else:
            try:
                format, imgstr = media_raw.split(';base64,') 
                ext = format.split('/')[-1] 
                file_data = ContentFile(base64.b64decode(imgstr), name=f'post_image.{ext}')

                # Сохраняем пост
                Posts.objects.create(title=title, text=text, media=file_data)
                return redirect('posts')
            except Exception as e:
                print(f"ПРОБЛЕМА ТУТ: {e}")
                error_message = f"Ошибка при обработке изображения: {e}"

    return render(request, 'posts/create.html', {'error': error_message})