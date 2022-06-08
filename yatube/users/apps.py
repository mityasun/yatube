from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = 'Управление пользователями'

    def ready(self):
        import users.signals
