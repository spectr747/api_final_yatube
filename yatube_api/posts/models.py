from django.db.models.deletion import CASCADE, SET_NULL
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    slug = models.SlugField(unique=True, default='-пусто-')
    title = models.CharField(
        max_length=200, 
        verbose_name='Наименование группы'
    )
    description = models.TextField(verbose_name='Описание группы')

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group,
        on_delete=SET_NULL,
        related_name='posts',
        null=True,
        blank=True,
        verbose_name='Группа'
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self) -> str:
        return self.text
        

class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='follower',
        null=True,
        blank=True,
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User, 
        on_delete=CASCADE,
        related_name='following',
        null=True,
        blank=True,
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['following', 'user'],
                name='unique_subscript')
        ]

    def __str__(self) -> str:
        return f'{self.user} пописан на {self.following}'
