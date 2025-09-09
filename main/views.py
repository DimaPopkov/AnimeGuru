from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse

from .models import Tags, Category, Product, Album_Pics, Characters
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

    #   Реализованно на JavaScript в Card.html
    #   max_len = 1500   # предел длины
    #   for idx, txt in enumerate(MainCharacters_desc):
    #       if len(txt) > max_len:               # только длинные строки
    #           # ищем последнюю точку до max_len
    #           period = txt.rfind('.', 0, max_len)
    #           if period != -1:                 # точка найдена
    #               MainCharacters_desc[idx] = txt[:period + 1]   # +1 – включаем точку
    #           else:                            # точек в пределах max_len нет
    #               MainCharacters_desc[idx] = txt[:max_len]
    #   i = 0
    #   for element in MainCharacters:
    #       element.description = MainCharacters_desc[i]
    #       i += 1
    #       print("\n\n\n", element, "\n\n" , element.description, "\n\n\n")

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