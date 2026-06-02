from django.db import models

from django.conf import settings

from django.contrib.auth import get_user_model

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
User = get_user_model()

# Create your models here.
class Posts(models.Model):
    title = models.TextField('Заголовок поста')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('Текст поста')
    media = models.ImageField('Медиа-файлы поста', null=True, blank=True)
    like_count = models.IntegerField('Кол-во лайков под постом', default=0, blank=True)
    dislike_count = models.IntegerField('Кол-во дизлайков под постом', default=0, blank=True)

    def __str__(self):
        return self.title
    
class PostsAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike'), ('none', 'None')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} {self.action_type}d on {self.post.id}"
    
class PostComment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('Текст комментария')
    like_count = models.IntegerField('Кол-во лайков под постом', default=0, blank=True)
    dislike_count = models.IntegerField('Кол-во дизлайков под постом', default=0, blank=True)
    state = models.BooleanField('True - like, False - dislike, None - not yet', null=True)
    parentId = models.IntegerField('ID родительского коммента (если нет - null/none)', null=True)
    locateZ = models.IntegerField('Z-index комментария относительно тайтла (0 уровень)', null=True)

    def __str__(self):
        return self.text