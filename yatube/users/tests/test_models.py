from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import User

User = get_user_model()


class UserModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='Author',
            first_name='Имя',
            last_name='Фамилия',
            email='test@test.com',
        )

    def test_models_have_correct_title_names(self):
        """Проверяем, что у модели корректно работает __str__."""
        title = (
            (self.user.username, 'Author'),
        )
        for name, expected_name in title:
            with self.subTest(expected_name=name):
                self.assertEqual(expected_name, str(name))

    def test_field_verboses_for_models(self):
        """Проверка verbose names."""
        field_verboses = {
            'profile_pic': 'Аватарка',
            'city': 'Город',
            'vk': 'Вконтакте',
            'telegram': 'Telegram',
            'instagram': 'Instagram',
            'git': 'Git',
        }
        for field, expected in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    User._meta.get_field(field).verbose_name, expected)
