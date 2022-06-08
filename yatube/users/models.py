from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    profile_pic = models.ImageField(
        'Аватарка',
        default='users/default.jpeg',
        upload_to='users/',
        null=True, blank=True,
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

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'
