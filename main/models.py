from django.db import models

from django.conf import settings

from django.contrib.auth import get_user_model

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
User = get_user_model()

class UserActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'date')  # один логин в день = одна запись
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['user', 'date']),
        ]

class AiMessages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.TextField(null=True, default="user")
    user_message = models.TextField()
    ai = models.TextField()
    ai_message = models.TextField()

    def __str__(self):
        return self.user.username

class Pics(models.Model):
    image = models.ImageField('Изображение', upload_to='img/pics/', null=True)
    def __str__(self):
        return self.image.name
    
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
    image = models.ImageField('Изображение', blank=True, null=True)
    season = models.DateField('Когда вышел (сезон)')
    tags = models.ManyToManyField(Tags, related_name='products')
    rating = models.TextField('Рейтинг', max_length=3)
    age_rating = models.IntegerField('Возрастной рейтинг')
    product_manager = models.CharField('Студия выпуска', max_length=100, null=True)
    episods = models.TextField('Кол-во эпизодов', null=True)
    status = models.ForeignKey(Status, null=True, on_delete=models.SET_NULL, related_name='products')
    trailer = models.URLField('Трейлер', blank=True, null=True)
    links = models.ManyToManyField(Weblinks, related_name='links', null=True)
    main_characters = models.ManyToManyField('Characters', related_name='main_characters', null=True)
    characters = models.ManyToManyField('Characters', related_name='other_characters', null=True)

    def __str__(self):
        return self.name

class Voice_maker(models.Model):
    first_name = models.TextField('Имя')
    second_name = models.TextField('Фамилия', null=True)
    age = models.IntegerField('Возраст', null=True)
    #products_in = models.ManyToManyField(Product, related_name="product_in")

    def __str__(self):
        return self.first_name

class Characters(models.Model):
    image = models.URLField('Картинка', blank=True, null=True)
    alter_pic = models.ImageField('Альтернативный доступ к картинке (если ссылка отвалилась)', blank=True, null=True)
    first_name = models.TextField('Имя')
    second_name = models.TextField('Фамилия', null=True)
    age = models.IntegerField('Возраст', null=True)
    description = models.TextField('Всё о герое, где появляется, что делал и т.д. и т.п.')
    products = models.ManyToManyField(Product, related_name='products_in')
    #voice_makers = models.ManyToManyField(Voice_maker, related_name='voices', null=True)
    link_to_wiki = models.URLField('Ссылка на вики', blank=True, null=True)

    def __str__(self):
        return self.first_name
    
class Comments(models.Model):
    name = models.TextField('Имя тайтла', null=True)
    user_image = models.ImageField('Image:', null=True)
    user_name = models.TextField('Логин пользователя:')
    user_rating = models.IntegerField('Оценка пользователя:', null=True)
    user_comment = models.TextField('Комментарий пользователя:', null=True)
    like_count = models.IntegerField('Кол-во лайков под постом')
    dislike_count = models.IntegerField('Кол-во дизлайков под постом')
    state = models.BooleanField('True - like, False - dislike, None - not yet', null=True)
    parentId = models.IntegerField('ID родительского коммента (если нет - null/none)', null=True)
    locateZ = models.IntegerField('Z-index комментария относительно тайтла (0 уровень)', null=True)

    def __str__(self):
        return self.name
    
class CommentAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike'), ('none', 'None')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment') # Гарантирует, что у пользователя будет только одно действие на комментарий

    def __str__(self):
        return f"{self.user.username} {self.action_type}d on {self.comment.id}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/', default="avatars/null_avatar.png", blank=True)
    favourites = models.ManyToManyField(Product)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()