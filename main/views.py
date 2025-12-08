from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.apps import apps
from django.db import models
from django.db.models import OuterRef, Subquery, FileField

from django.contrib.auth.models import User

from .models import Tags, Category, Product, Album_Pics, Characters, Comments, CommentAction 
from .forms import ProductForm
import re, requests

# Create your views here.
def main(request):
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
    }
        
    return render(request, 'main/main.html', data)

def about(request):
    data = {
        'title' : 'О нас'
    }

    return render(request, 'main/about.html', data)

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
    products = Product.objects.all()
    finalTags = Tags.objects.all().order_by('name')

    # Фильтр по категории
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    tags_ids = request.GET.getlist('tags')
    if tags_ids:
        for tag_id in tags_ids:
            products = products.filter(tags__id=tag_id)
        products = products.distinct()

    status_id = request.GET.get('activeStatus')
    if status_id:
        products = products.filter(status_id=status_id)

    filter_data = [category_id, tags_ids, status_id]

    selected_category = category_id
    selected_tags = tags_ids
    selected_status = status_id

    context = {
        'title' : 'Основная страница',
        'categories' : Category.objects.all(),
        'products': products,
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

    # Находим пересечение множеств токенов
    common_tokens = tokens1.intersection(tokens2)

    # Степень схожести: (кол-во общих слов) / (мин. кол-во слов в одном из названий)
    # Можно также использовать (кол-во общих слов) / (среднее кол-во слов) или (общее кол-во уникальных слов)
    # Использование min() помогает учитывать названия разной длины
    similarity_score = len(common_tokens) / min(len(tokens1), len(tokens2))

    return similarity_score

def card(request, product_name):
    products = get_object_or_404(Product, name=product_name)

    comments = Comments.objects.filter(name=product_name).annotate(net_likes=models.F('like_count') - models.F('dislike_count'))

    CurrentUserName = request.user.username
    print(CurrentUserName)

    CurrentComment = None

    for comment in comments:
        if comment.user_name == CurrentUserName:
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
    print("\n\n", allComments)
    allComments_state = CommentAction.objects.filter(user=request.user)
    print("\n\n", allComments_state)

    focus_comment_state = []
    for product_state in allComments_state:
        if product_state.comment.name == products.name:
            if product_state.action_type == "like":
                focus_comment_state.append(2)
            elif product_state.action_type == "dislike":
                focus_comment_state.append(1)
            else:
                focus_comment_state.append(0)

    print(focus_comment_state)

    zipped_items = zip(comments, focus_comment_state)
    print(zipped_items)

    # allComments = CommentAction.objects.filter(user=request.user)
    # print(allComments, "\n\n")

    # i = 0
    # comment_state = [0] * allComments.__len__() # 0 - нет данных, 2 - Like, 1 - Dislike
    # print(comment_state)

    # for element in allComments:
    #     if element.comment.name == products.name:
    #         print(element.action_type)
    #         if element.action_type == "like":
    #             comment_state[i] = 2
    #         elif element.action_type == "dislike":
    #             comment_state[i] = 1
    #     else:
    #         print("Комментарий не подходит: ", element.comment, " ", products)
    #     i += 1

    # print(comment_state)

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
        'comments': comments,
        'zipped_items': zipped_items,
        'your_comment': CurrentComment,
        'star_list': star_list,
        'most_popular_comment': most_popular_comment,
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
        Product.objects.filter(name=OuterRef('name')).values('image')[:1] # [:1] берет первое совпадение
    )

    product_category_subquery = Subquery(
        Product.objects.filter(name=OuterRef('name')).values('category__name')[:1] # [:1] берет первое совпадение
    )

    product_rating_subquery = Subquery(
        Product.objects.filter(name=OuterRef('name')).values('rating')[:1] # [:1] берет первое совпадение
    )

    product_season_subquery = Subquery(
        Product.objects.filter(name=OuterRef('name')).values('season')[:1] # [:1] берет первое совпадение
    )
    
    allComents = Comments.objects.filter(user_name=username).annotate(
        product_image=product_image_subquery,
        product_category=product_category_subquery,
        product_rating=product_rating_subquery,
        net_likes=models.F('like_count') - models.F('dislike_count'),
        product_season=product_season_subquery,
    )
    
    star_list = list(range(1, 11))

    context = {
        'title' : 'Личный кабинет',
        'your_comments': allComents,
        'star_list': star_list,
    }

    return render(request, 'main/profile.html', context)

def add_comments(request, product_name):

    product = get_object_or_404(Product, name=product_name)

    #Comments.objects.all().delete() # Очистка таблицы

    User_comment = request.POST.get('text')
    User_rating = request.POST.get('rating')

    user_name = request.user.username
    user_image = request.user.profile.image

    new_comment = Comments(
        name = product,
        user_image = user_image,
        user_name = user_name,
        user_rating = User_rating,
        user_comment = User_comment,
        like_count = 0,
        dislike_count = 0,
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
        print("ФОТКА ДОШЛА")

        username = request.POST.get('user_id')
        image_file = request.POST.get('image') # получение фотки
        print(image_file)

        if not username or not image_file:
            return JsonResponse({'error': 'Недостаточно данных для обновления аватара.'}, status=400)

        try:
            # Получаем конкретного пользователя
            user = User.objects.get(username=username)

            # Присваиваем файл изображению в профиле
            user.profile.image = image_file
            print(image_file)
            user.profile.save()

            print(f"Аватар успешно обновлен для пользователя: {username}")

            # Возвращаем URL изображения
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