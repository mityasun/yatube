from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая запись',
        )

    def test_models_have_correct_title_names(self):
        """Проверяем, что у моделей Group и Post корректно работает __str__."""
        title = (
            (self.group, self.group.title),
            (self.post, self.post.text[:settings.CUT_TEXT]),
        )
        for text, expected_name in title:
            with self.subTest(expected_name=text):
                self.assertEqual(expected_name, str(text))

    def test_field_verboses_for_models(self):
        """Проверка verbose names."""
        post = self.post
        field_verboses = {
            'author': 'Автор',
            'text': 'Текст записи',
            'pub_date': 'Дата публикации',
            'group': 'Выберите сообщество:',
            'image': 'Картинка',
        }
        for field, expected in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected)

    def test_help_texts_for_models(self):
        """Проверка help_text."""
        post = self.post
        field_help_texts = {
            'group': 'Сообщество для вашей записи',
            'text': 'Текст вашей записи',
            'image': 'Добавить картинку',
        }
        for field, expected in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected)
