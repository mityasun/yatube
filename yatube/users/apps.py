from django.apps import AppConfig
from django.db.models.signals import post_migrate


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = 'Управление пользователями'

    def ready(self):
        from .signals import create_profile, save_profile
        post_migrate.connect(create_profile, sender=self)
        post_migrate.connect(save_profile, sender=self)
