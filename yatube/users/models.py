from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_pic = models.ImageField(
        'Аватарка',
        default='users/default.jpeg',
        upload_to='users/',
        null=True, blank=True,
        help_text='Добавить аватарку',
    )
    city = models.CharField('Город', max_length=50, null=True, blank=True)
    vk = models.CharField('Вконтакте', max_length=50, null=True, blank=True)
    telegram = models.CharField(
        'Telegram',
        max_length=50,
        null=True, blank=True,
    )
    instagram = models.CharField(
        'Instagram',
        max_length=50,
        null=True, blank=True,
    )
    git = models.CharField('Git', max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username
