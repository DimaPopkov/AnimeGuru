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

from .models import Posts, PostsAction, PostComment
import re, json, requests, Levenshtein

# Create your views here.
def posts(request):
    allPosts = list(Posts.objects.all())

    allPosts_state = []
    if request.user.is_authenticated:
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

    comments = PostComment.objects.filter(post=post)

    CurrentComment = None

    for comment in comments:
        if comment.user.username == request.user.username:
            if(comment.locateZ == 0):
                CurrentComment = comment

    data = {
        'title': post.title,
        'post': post,
        'comments': comments,
        'your_comment': CurrentComment,
    }
        
    return render(request, 'posts/post.html', data)

def update_post_state(request, post_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)
    
    if request.user.is_authenticated:
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
                'like_count': post.like_count,
                'dislike_count': post.dislike_count,
                'existing_action': existing_action.action_type
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return redirect('login')
    
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

        if not title:
            error_message = "Вы не ввели заголовок"
        elif not text:
            error_message = "Поле текста не может быть пустым"
        elif not media_raw:
            error_message = "Забыли загрузить обложку"
        else:
            try:
                file_data = None

                if media_raw and media_raw != 'none':
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

def add_comment(request, post_id):
    try:
        post = get_object_or_404(Posts, id=post_id)   
    except:
        post = None

    try:
        text = request.POST.get('text')
    except:
        text = None 

    try:
        parentId = request.POST.get('parentId')
        parentComment = PostComment.objects.get(id=parentId)
        locateZ_find = int(parentComment.locateZ) + 1    
    except:
        parentId = None
        locateZ_find = 0

    new_comment = PostComment(
        post = post,
        user = request.user,
        text = text,
        like_count = 0,
        dislike_count = 0,
        parentId = parentId,
        locateZ = locateZ_find,
    )

    new_comment.save()

    url_to_redirect_to = reverse('post', kwargs={'post_id': post.id})
    url_with_anchor = f"{url_to_redirect_to}#comment-{new_comment.id}"
    return redirect(url_with_anchor)

def edit_comment(request, post_id):
    post = Posts.objects.get(id=post_id)

    try:
        existing_comment = PostComment.objects.get(post=post, user=request.user)
    except Posts.DoesNotExist:
        url_to_redirect_to = reverse('post', kwargs={'post_id': post_id})
        return redirect(url_to_redirect_to)

    new_comment_text = request.POST.get('text')

    existing_comment.text = new_comment_text

    existing_comment.save()

    print("\n\n------------- Edited_Comment ----------------\n", existing_comment)

    url_to_redirect_to = reverse('post', kwargs={'post_id': post_id})
    url_with_anchor = f"{url_to_redirect_to}#comment-{existing_comment.id}"
    return redirect(url_with_anchor)

def delete_comment(request, post_id):
    user_name = request.user.username

    post = Posts.objects.get(id=post_id)

    try:
        existing_comment = PostComment.objects.get(post=post, user=request.user)
    except PostComment.DoesNotExist:
        url_to_redirect_to = reverse('card', kwargs={'post_id': post_id})
        return redirect(url_to_redirect_to)
    
    existing_comment.delete()
    print("Комментарий успешно удалён!")
    
    # url_to_redirect_to = reverse('card', kwargs={'product_name': product_name})
    return redirect(request.META.get('HTTP_REFERER', '/'))