<p align="center"><a href="https://www.djangoproject.com/" target="_blank"><img src="https://static.djangoproject.com/img/logo-django.42234b631760.svg" width="400" alt="Django Logo"></a></p>

# Необходимые пакеты и зависимости

Django:
```pip install django```

Django Unfold:
```pip install django-unfold```

Requests:
```pip install requests```

Levenshtein:
```pip install python-Levenshtein```

Pillow:
```pip install Pillow```

# Доступные методы

Доступен метод ```python manage.py load_anime``` для добавления новых тайтлов в каталог 

*Прежде чем его использовать, заполните data.json в корне проекта необходимыми данными

```
data.json
[
    {
        "name": "Основное название" (Обязательное поле),
        "eng_name": "Английское название" (null=True),
        "description": "Описание тайтла" (null=True),
        "season_info": "Пересказ сезона" (null=True),
        "category": "ТВ Сериал" (Обязательное поле),
        "image": "Обложка.webp (Должна лежать в media)" (null=True),
        "season": "YYYY-MM-DD (null=True)",
        "tags": ["Тег", "Тег"] или "Тег" (null=True),
        "rating": Float (null=True),
        "age_rating": Integer (null=True),
        "product_manager": "Название" (null=True),
        "episods": "Integer" (null=True),
        "status": "Вышел \ Онгоинг \ Выходит" (null=True),
        "trailer": "Ссылка на трейлер" (null=True),
        "links": "Ссылки на сторонние сайты с плеером для просмотра" (null=True),
        "main_characters": "" (Оставьте этот пункт пустым),
        "characters": "" (Оставьте этот пункт пустым),
        "pics_name": ["Название", Количество] (Фотографии для слайдера, должны храниться в media\img\pics и иметь названия "название_pic1" \ "название_pic2" и т.п.) (Количество - число фотографий в папке media) (null=True)
    }
]
```
