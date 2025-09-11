from django.db import models

# Create your models here.
class Pics(models.Model):
    image = models.URLField('Изображение', blank=True, null=True)
    def __str__(self):
        return self.image
    
class Album_Pics(models.Model):
    name = models.TextField('Название Альбома (для какого тайтла)', null=True)
    image = models.ManyToManyField(Pics, related_name='pics')
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField('Тэг', max_length=50)

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField('Тэг', max_length=50)

    def __str__(self):
        return self.name

class Weblinks(models.Model):
    name = models.TextField('Название сайта', null=True)
    link = models.TextField('Ссылка на сайт:', null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField('Название', max_length=100)
    eng_name = models.CharField('Английское название', max_length=100, null=True)
    description = models.TextField('Описание')
    season_info = models.TextField('Пересказ сезона:', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.URLField('Изображение', blank=True, null=True)
    season = models.DateField('Когда вышел (сезон)')
    tags = models.ManyToManyField(Tags, related_name='products')
    rating = models.TextField('Рейтинг', max_length=3)
    age_rating = models.IntegerField('Возрастной рейтинг')
    product_manager = models.CharField('Студия выпуска', max_length=100, null=True)
    episods = models.TextField('Кол-во эпизодов', null=True)
    status = models.ForeignKey(Status, null=True, on_delete=models.SET_NULL, related_name='products')
    trailer = models.URLField('Трейлер', blank=True, null=True)
    links = models.ManyToManyField(Weblinks, related_name='links')
    main_characters = models.ManyToManyField('Characters', related_name='main_characters')
    characters = models.ManyToManyField('Characters', related_name='other_characters')
    comments = models.ManyToManyField('Comments', related_name='comments')

    def __str__(self):
        return self.name

class Voice_maker(models.Model):
    first_name = models.TextField('Имя')
    second_name = models.TextField('Фамилия', null=True)
    age = models.IntegerField('Возраст', null=True)
    products_in = models.ManyToManyField(Product, related_name="product_in")

    def __str__(self):
        return self.first_name

class Characters(models.Model):
    image = models.URLField('Картинка', blank=True, null=True)
    first_name = models.TextField('Имя')
    second_name = models.TextField('Фамилия', null=True)
    age = models.IntegerField('Возраст', null=True)
    description = models.TextField('Всё о герое, где появляется, что делал и т.д. и т.п.')
    products = models.ManyToManyField(Product, related_name='products_in')
    #close_charecters = models.ManyToManyField(Characters, , related_name='simps')
    voice_makers = models.ManyToManyField(Voice_maker, related_name='voices')
    link_to_wiki = models.URLField('Ссылка на вики', blank=True, null=True)

    def __str__(self):
        return self.first_name
    
class Comments(models.Model):
    product_name = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name='product_name')
    user_name = models.TextField('Логин пользователя:')
    user_rating = models.IntegerField('Оценка пользователя:')
    user_comment = models.TextField('Комментарий пользователя:', null=True)

    def __str__(self):
        return self.product_name