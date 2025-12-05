from django.db import models

from django.utils import timezone
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
User = get_user_model()
class UserActivity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='activity')
    last_login_date = models.DateField(default=timezone.now().date())
    login_count_today = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Activity for {self.user.username}"

    def update_activity(self):
        today = timezone.now().date()
        if self.last_login_date != today:
            self.last_login_date = today
            self.login_count_today = 1
        else:
            self.login_count_today += 1
        self.save()


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
    name = models.TextField('Имя тайтла', null=True)
    user_image = models.ImageField('Image:', null=True)
    user_name = models.TextField('Логин пользователя:')
    user_rating = models.IntegerField('Оценка пользователя:')
    user_comment = models.TextField('Комментарий пользователя:', null=True)
    like_count = models.IntegerField('Кол-во лайков под постом')
    dislike_count = models.IntegerField('Кол-во дизлайков под постом')
    state = models.BooleanField('True - like, False - dislike, None - not yet', null=True)

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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()