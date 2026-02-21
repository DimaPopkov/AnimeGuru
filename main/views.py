from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.apps import apps
from django.db import models
from django.db.models import OuterRef, Subquery, FileField
from django.core.cache import cache

from django.contrib.auth.models import User

from .models import Tags, Category, Product, Album_Pics, Characters, Comments, CommentAction, AiMessages
from .forms import ProductForm
import re, json, requests, Levenshtein

# Create your views here.
def main(request):
    try:
        theme = request.session['courent_theme']
    except:
        theme = request.session.get('courent_theme', 'black')
        request.session['courent_theme'] = 'black'

    print('Текущая тема: ', request.session.get('courent_theme', 'black'))
    allProducts = Product.objects.all()
    
    Allstatus = []

    for element in allProducts:
        if element.status not in Allstatus:
            Allstatus.append(element.status)

    data = {
        'title' : 'Основная страница',
        'categories' : Category.objects.all().order_by('-name'),
        'products' : allProducts,
        'tags': Tags.objects.all().order_by('name'),
        'status': Allstatus,
        'theme': theme
    }
        
    return render(request, 'main/main.html', data)

def about(request):
    data = {
        'title' : 'О нас'
    }

    return render(request, 'main/about.html', data)

def courent_theme(request):
    return request.session['courent_theme']

def save_theme(request):
    courent_theme_name = request.POST.get('theme_content')
    request.session['courent_theme'] = courent_theme_name
    print(courent_theme_name)
    return JsonResponse({'success': True, 'theme': courent_theme_name}, status=200)

def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
        
    data = {
        'title' : 'Добавление',
        'form' : ProductForm()
    }

    return render(request, 'main/create.html', data)

def filter(request):
    final_products = []
    products = Product.objects.all()
    finalTags = Tags.objects.all().order_by('name')

    # Фильтр по категории
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    # Фильтр по тегам
    tags_ids = request.GET.getlist('tags')
    if tags_ids:
        for tag_id in tags_ids:
            products = products.filter(tags__id=tag_id)
        products = products.distinct()

    # Фильтр по статусу
    status_id = request.GET.get('activeStatus')
    if status_id:
        products = products.filter(status_id=status_id)

    # Фильтр по названию
    titlename = request.GET.get('titlename')
    similarity_threshold_char = 0.3
    similarity_threshold = 0.3

    if titlename:
        for product in products:
            array = product.name.split(" ")
            if array.__len__() == 1:
                similarity_threshold_final = calculate_char_similarity(product.name, titlename)
                if similarity_threshold_final >= similarity_threshold_char:
                    final_products.append(product)

            else:
                similarity_threshold_final = calculate_similarity(product.name, titlename)
                if similarity_threshold_final >= similarity_threshold:
                    final_products.append(product)

    else:
        final_products = products

    filter_data = [category_id, tags_ids, status_id]

    selected_category = category_id
    selected_tags = tags_ids
    selected_status = status_id

    context = {
        'title' : 'Основная страница',
        'categories' : Category.objects.all(),
        'products': final_products,
        'tags': finalTags,
        'filter_data': filter_data,
        'selected_category': selected_category,
        'selected_tags': selected_tags,
        'selected_status': selected_status,
    }
    
    return render(request, 'main/main.html', context)

def normalize_name(name):
    """
    Приводит название к нижнему регистру, удаляет пунктуацию и разбивает на слова.
    """
    name = name.lower()
    # Удаляем знаки препинания, кроме дефисов, если они внутри слова
    name = re.sub(r'[^\w\s-]', '', name)
    # Разбиваем на слова, учитывая дефисы как часть слова, если они не по краям
    tokens = re.findall(r'\b[\w-]+\b', name)
    return set(tokens) # Возвращаем множество для быстрого поиска пересечения

def calculate_similarity(name1, name2):
    """
    Рассчитывает степень схожести названий на основе общих слов.
    Возвращает долю общих слов от общего числа слов.
    """
    tokens1 = normalize_name(name1)
    tokens2 = normalize_name(name2)

    if not tokens1 or not tokens2: # Если одно из названий пустое после нормализации
        return 0.0

    char_similarity_score = 1
    for word_name1 in name1:
        for word_name2 in name2:
            char_similarity_score += calculate_char_similarity(word_name1, word_name2)

    # Находим пересечение множеств токенов
    common_tokens = tokens1.intersection(tokens2)


    # Степень схожести: (кол-во общих слов) / (мин. кол-во слов в одном из названий)
    similarity_score = (len(common_tokens) / min(len(tokens1), len(tokens2))) + len(common_tokens) / char_similarity_score

    return similarity_score

def calculate_char_similarity(name1, name2):
    """
    Рассчитывает степень схожести двух строк на основе расстояния Левенштейна.

    Схожесть = 1 - (Расстояние Левенштейна / Максимальная длина строки)

    Возвращает значение от 0.0 (полное несовпадение) до 1.0 (полное совпадение).
    """
    # Приводим строки к нижнему регистру для регистронезависимого сравнения
    s1 = name1.lower()
    s2 = name2.lower()

    # 1. Вычисляем расстояние Левенштейна
    distance = Levenshtein.distance(s1, s2)

    # 2. Определяем максимальную возможную длину (для нормализации)
    max_len = max(len(s1), len(s2))

    # Обе строки пустые
    if max_len == 0:
        return 1.0

    # 3. Нормализуем расстояние, чтобы получить коэффициент схожести
    # Схожесть = 1 - (Расстояние / Максимальная длина)
    similarity_score = 1.0 - (distance / max_len)

    return similarity_score

def card(request, product_name):
    products = get_object_or_404(Product, name=product_name)

    comments = Comments.objects.filter(name=product_name).annotate(net_likes=models.F('like_count') - models.F('dislike_count'))

    CurrentUserName = request.user.username
    print(CurrentUserName)

    CurrentComment = None

    for comment in comments:
        if comment.user_name == CurrentUserName:
            if(comment.locateZ == 0):
                CurrentComment = comment
                print("CurrentComment: ", CurrentComment.user_comment)

    star_list = list(range(1, 11))
    print(star_list)

    most_popular_comment = 0

    for element in comments:
        if most_popular_comment != 0 and element.net_likes > most_popular_comment.net_likes:
            most_popular_comment = element
        elif most_popular_comment == 0:
            most_popular_comment = element

    print(products)
    selected_product = Product.objects.get(name=products)

    if selected_product.eng_name:
        product_link_name = selected_product.eng_name.lower().split(',')
    else: product_link_name = "null"

    print(product_link_name)
    #translator = Translator(from_lang="ru", to_lang="en")
    #English_product_name = translator.translate(product_link_name)
    #print(English_product_name)

    MainCharacters_desc = []

    MainCharacters = products.main_characters.all()
    print(products.main_characters.all())

    for element in MainCharacters:
        try:
            # ищем запись в Characters, у которой совпадает first_name
            character = Characters.objects.get(first_name=element.first_name)
        except Characters.DoesNotExist:
            # если подобного персонажа нет – пропускаем
            continue

        # добавляем описание в список
        MainCharacters_desc.append(character.description)

    other_characters = products.characters.exclude(
        id__in=products.main_characters.values_list('id', flat=True)
    )

    print("Главные герои: ", products.main_characters.all(), "\n", "Другие герои: ", other_characters)

    FinalAlbumPics = Album_Pics.objects.all().order_by('name')

    try:
        All_Albums_pic = FinalAlbumPics.get(name=products)
        all_pics = All_Albums_pic.image.all()
    except:
        all_pics = "none"
    
    product_tags = selected_product.tags.all()
    product_links = selected_product.links.all()
    print(product_links)

    #Собираем строку "tag_names" со всеми тэгами
    tag_namesArray = [tags.name for tags in product_tags]
    tag_names = ", ".join(tag_namesArray)

    #Собираем строку "season_final" с описанием сезона по типу "Осень 2006"
    product_date = selected_product.season
    if not product_date:
        return JsonResponse({'success': False, 'error': f"У продукта '{selected_product.name}' не указана дата сезона."}, status=400)

    year = product_date.year

    month = product_date.month
    season = ""

    if 3 <= month <= 5:
        season = "Весна"
    elif 6 <= month <= 8:
        season = "Лето"
    elif 9 <= month <= 11:
        season = "Осень"
    else:
        season = "Зима"

    season_final = f"{season} {year}"

    # Получаем все тайтлы
    all_products = Product.objects.all()
    # Получаем имя выбранного тайтла
    target_product_name = selected_product.name
    
    for p in all_products:
        if p.name.lower() == target_product_name.lower():
            target_product_instance = p
            break

    related_products = []
    similarity_threshold = 0.5 

    for product in all_products:
        # Пропускаем сам целевой продукт
        if target_product_instance and product.name == target_product_instance.name:
            continue

        # Рассчитываем степень схожести
        similarity = calculate_similarity(target_product_name, product.name)

        # Если схожесть выше порога, добавляем продукт
        if similarity >= similarity_threshold:
            related_products.append(product)

    # Смотрим, если есть комментарии которые мы лайкали\дизлайкали, то меняем им иконки
    allComments = Comments.objects.filter(name=products.name)
    print("\n------------------------\n", 
        allComments)
    
    allComments_state = CommentAction.objects.filter(user=request.user)
    print("\n------------------------\n",
        allComments_state, "\n")

    focus_comment_state = []

    for comment in allComments:
        for comment_action in allComments_state:
            # print(comment_action.comment.name, "\n", comment.name)
            if comment_action.comment.name == comment.name:
                # print(comment_action.comment, "\n", comment)
                if comment_action.action_type == "like":
                    focus_comment_state.append(2)
                elif comment_action.action_type == "dislike": 
                    focus_comment_state.append(1)
                else:
                    focus_comment_state.append(0)
        if focus_comment_state == []:
            for element in allComments:
                focus_comment_state.append(0)

    zipped_items = list(zip(comments, focus_comment_state))
    print(zipped_items)

    context = {
        'title' : selected_product.name,
        'product': selected_product,
        'product_tags': tag_names,
        'season': season_final,
        'pics': all_pics,
        'related_products': related_products,
        'links': product_links,
        'link_name': product_link_name,
        'main_characters': MainCharacters,
        'characters': other_characters,
        'comments': allComments,
        'zipped_items': zipped_items,
        'zipped_items2': zipped_items,
        'zipped_items3': zipped_items,
        'your_comment': CurrentComment,
        'star_list': star_list,
        'most_popular_comment': most_popular_comment,
        'AI_models': ["gemma3:12b", "deepseek-r1:14b", "qwen:0.5b"],
        'theme': request.session.get('courent_theme', 'black'),
        #'AI_models': {"gemma3:4b", "gemma3:12b"},
    }
    print("\n\n", request, "\n Метод POST \n")
    print("Сохранено:", target_product_name, "\n")

    return render(request, 'main/card.html', context)

def check_url(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("Ссылка работает!")
        else:
            print(f"Ошибка: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения: {e}")

def profile(request):
    username = request.user.username

    product_image_subquery = Subquery(
        Product.objects.filter(name=OuterRef('name')).values('image')
    )

    product_category_subquery = Subquery(
        Product.objects.filter(name=OuterRef('name')).values('category__name')
    )

    product_rating_subquery = Subquery(
        Product.objects.filter(name=OuterRef('name')).values('rating')
    )

    product_season_subquery = Subquery(
        Product.objects.filter(name=OuterRef('name')).values('season')
    )

    allComents = Comments.objects.filter(user_name=username).annotate(
        product_image = product_image_subquery,
        product_category = product_category_subquery,
        product_rating = product_rating_subquery,
        net_likes = models.F('like_count') - models.F('dislike_count'),
        product_season=product_season_subquery,
    )
    
    star_list = list(range(1, 11))

    context = {
        'title' : 'Личный кабинет',
        'your_comments': allComents,
        'star_list': star_list,
        'favourites': None,
    }

    return render(request, 'main/profile.html', context)

def add_comments(request, product_name):

    product = get_object_or_404(Product, name=product_name)

    #Comments.objects.all().delete() # Очистка таблицы

    try:
        User_comment = request.POST.get('text')
    except:
        User_comment = None

    try:
        User_rating = request.POST.get('rating')
    except:
        User_rating = 0

    try:
        parentId = request.POST.get('parentId')
        parentComment = Comments.objects.get(id=parentId)
        locateZ_find = int(parentComment.locateZ) + 1    
    except:
        parentId = None
        locateZ_find = 0

    user_name = request.user.username
    user_image = request.user.profile.image

    print("product: ", product, "\nUser_comment: ", User_comment, "\nUser_rating: ", User_rating, "\nuser_name: ", user_name, "\nparentId: ", parentId)


    new_comment = Comments(
        name = product,
        user_image = user_image,
        user_name = user_name,
        user_rating = User_rating,
        user_comment = User_comment,
        like_count = 0,
        dislike_count = 0,
        parentId = parentId,
        locateZ = locateZ_find,
    )

    new_comment.save()

    print("Комментарий для ", product_name, " добавлен")

    url_to_redirect_to = reverse('card', kwargs={'product_name': product_name})
    return redirect(url_to_redirect_to)

def edit_comments(request, product_name):

    user_name = request.user.username

    try:
        existing_comment = Comments.objects.get(name=product_name, user_name=user_name)
    except Comments.DoesNotExist:
        url_to_redirect_to = reverse('card', kwargs={'product_name': product_name})
        return redirect(url_to_redirect_to)

    new_rating = request.POST.get('rating')

    if ((new_rating == None) or (new_rating == '')):
        new_rating = 0

    new_comment_text = request.POST.get('text')

    # Обновляем поля существующего комментария
    existing_comment.user_rating = new_rating
    existing_comment.user_comment = new_comment_text

    existing_comment.save()

    print("\n\n------------- Edited_Comment ----------------\n", existing_comment)

    url_to_redirect_to = reverse('card', kwargs={'product_name': product_name})
    return redirect(url_to_redirect_to)

def delete_comments(request, product_name):
    
    user_name = request.user.username

    try:
        existing_comment = Comments.objects.get(name=product_name, user_name=user_name)
    except Comments.DoesNotExist:
        url_to_redirect_to = reverse('card', kwargs={'product_name': product_name})
        return redirect(url_to_redirect_to)
    
    existing_comment.delete()
    print("Комментарий успешно удалён!")
    
    url_to_redirect_to = reverse('card', kwargs={'product_name': product_name})
    return redirect(url_to_redirect_to)

def update_comment_state(request, comment_id):
    if request.method == 'POST':      
        try:
            action = request.POST.get("action_ty")
            product_name = request.POST.get("product_name")

            AllComments = Comments.objects.filter(name=product_name).annotate(net_likes=models.F('like_count') - models.F('dislike_count'))
            comments = get_object_or_404(AllComments, id=comment_id)
            try:
                existing_action = CommentAction.objects.get(user=request.user, comment=comments)
            except: 
                existing_action = CommentAction.objects.create(user=request.user, comment=comments, action_type='none')

            existing_action_user = existing_action.user
            existing_action_comment = existing_action.comment
            existing_action_action_type = existing_action.action_type

            if action == "like":
                if existing_action and existing_action.action_type == "like":
                    existing_action.action_type = "none"
                    existing_action.save()

                    comments.like_count -= 1
                    comments.save()

                    AllComments = Comments.objects.filter(name=product_name).annotate(net_likes=models.F('like_count') - models.F('dislike_count'))
                    comments = get_object_or_404(AllComments, id=comment_id)      

                elif existing_action and existing_action.action_type == "dislike":
                    existing_action.action_type = "like"
                    existing_action.save()

                    comments.dislike_count -= 1
                    comments.like_count += 1    # Увеличиваем лайк

                    comments.save()

                    AllComments = Comments.objects.filter(name=product_name).annotate(net_likes=models.F('like_count') - models.F('dislike_count'))
                    comments = get_object_or_404(AllComments, id=comment_id)
                else:
                    existing_action.action_type = 'like'
                    existing_action.save()

                    comments.like_count += 1
                    comments.save()

                    AllComments = Comments.objects.filter(name=product_name).annotate(net_likes=models.F('like_count') - models.F('dislike_count'))
                    comments = get_object_or_404(AllComments, id=comment_id)

            elif action == "dislike":
                if existing_action and existing_action.action_type == "dislike":
                    existing_action.action_type = "none"
                    existing_action.save()

                    comments.dislike_count -= 1
                    comments.save()

                    AllComments = Comments.objects.filter(name=product_name).annotate(net_likes=models.F('like_count') - models.F('dislike_count'))
                    comments = get_object_or_404(AllComments, id=comment_id)

                elif existing_action and existing_action.action_type == "like":
                    # Пользователь сначала лайкнул, теперь дизлайкает
                    existing_action.action_type = "dislike"
                    existing_action.save()

                    comments.like_count -= 1
                    comments.dislike_count += 1 # Увеличиваем дизлайк
                    comments.save()

                    AllComments = Comments.objects.filter(name=product_name).annotate(net_likes=models.F('like_count') - models.F('dislike_count'))
                    comments = get_object_or_404(AllComments, id=comment_id)
                
                else:
                    existing_action.action_type = 'dislike'
                    existing_action.save()

                    comments.dislike_count += 1
                    comments.save()

                    AllComments = Comments.objects.filter(name=product_name).annotate(net_likes=models.F('like_count') - models.F('dislike_count'))
                    comments = get_object_or_404(AllComments, id=comment_id)
            else:
                return JsonResponse({'error': 'Invalid action'}, status=400)
        except:
            return JsonResponse({'error': 'Failed to load action'}, status=400)

        return JsonResponse({
            'comment': "",
            'status': 'success',
            'net_likes': comments.net_likes,
            'existing_action': existing_action.action_type
        })
    else:
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)
    
def profile_change_avatar(request):
    if request.method == 'POST':
        username = request.POST.get('user_id')
        image_file = request.POST.get('image')
        print(image_file)

        if not username or not image_file:
            return JsonResponse({'error': 'Недостаточно данных для обновления аватара.'}, status=400)

        try:
            # Получаем конкретного пользователя
            user = User.objects.get(username=username)

            # Присваиваем файл изображению в профиле
            user.profile.image = image_file
            user.profile.save()

            print(f"Аватар успешно обновлен для пользователя: {username}")

            return JsonResponse({
                'image_url': user.profile.image.url if user.profile.image else None,
            })

        except User.DoesNotExist:
            return JsonResponse({'error': f'Пользователь с именем "{username}" не найден.'}, status=404)
        except Exception as e:
            print(f"Произошла ошибка при обновлении аватара: {e}")
            return JsonResponse({'error': 'Произошла внутренняя ошибка сервера.'}, status=500)

    # Если запрос не POST, возвращаем ошибку или пустой ответ
    return JsonResponse({'error': 'Метод запроса не поддерживается.'}, status=405)

def AIchat(request):
    json_data = json.loads(request.body)

    json_data[0]['person'] = request.user.username

    AiMessages.objects.create(
        user = request.user,
        role = "user",
        user_message = json_data[0]['message'],
        ai = json_data[1]['person'],
        ai_message = json_data[1]['message'],
    )

    with open('lib.json', 'a', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False)
        f.write('\n')

    return JsonResponse({'status': 'success', 'message': 'Data saved successfully'})

def AIhistory(request):
    user_history = AiMessages.objects.filter(user=request.user)

    user_history_final = []
    
    for element in user_history:
        user_history_final.append(
            {
                "role" : "user", 
                "content" : element.user_message
            },
        )

    if(user_history_final == []):
        system_prompt = AiMessages.objects.create(
            user = request.user,
            role = "system",
            user_message = 'Ты - AI ассистент на сайте по поиску Аниме, Кино и Манги. Поддерживай деловой стиль общения с пользователем. Главное правило чата для тебя - Отвечать только на вопрос пользователя. Остальные правила чата с пользователем: - Не используй смайлики в ответах. - Тебе нельзя грубить пользователю. - Ты должен отвечать на вопросы пользователя четко и правильно. - Нельзя общаться про политику. - Если пользователь хвалит тебя, то поблагодари его и расскажи что ты можешь. - Переспрашивай пользователя, если ты не понял его сообщение. - Не упоминай политику в своих ответах. - Если пользователь задаёт вопрос не по темам сайта (Аниме, Кино и Манга), то напомни ему, на что ты можешь отвечать. - Не напоминай пользователю о своём функционале.',
            ai = "",
            ai_message = "",
        )
        system_prompt.save()

    print(user_history_final)
    # data = list(user_history.values())

    return JsonResponse(user_history_final, safe=False)

# def chat_view(request):
#     # Получаем сообщение пользователя
#     user_message = request.POST.get('message', '').strip()
#     if not user_message:
#         return JsonResponse({'error': 'Empty message'}, status=400)

#     # Получаем историю и форматируем для Ollama
#     history = get_user_history(request.user)
#     ollama_messages = format_for_ollama(history)

#     # Добавляем текущее сообщение
#     ollama_messages.append({
#         "role": "user",
#         "content": user_message
#     })

#     # Получаем ответ от Ollama
#     ai_response = call_ollama_api(ollama_messages)

#     if not ai_response:
#         return JsonResponse({'error': 'AI service unavailable'}, status=503)

#     # Сохраняем вопрос\ответ
#     massages = AiMessages.objects.create(
#         user = request.user,
#         user_message = user_message,
#         ai = "gemma3:12b",
#         ai_message = ai_response,
#     )

#     # Очищаем кэш истории
#     cache.delete(f"chat_history_{request.user.id}")

#     return JsonResponse({
#         'response': ai_response,
#         'message_id': massages.id
#     })
