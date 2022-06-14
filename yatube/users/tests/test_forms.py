import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..models import User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class UserFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='Author',
            first_name='Имя',
            last_name='Фамилия',
            email='test@test.com',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_edit_profile(self):
        """Проверка формы профиля."""
        bytes_image = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        image = SimpleUploadedFile(
            name='new_avatar.gif',
            content=bytes_image,
            content_type='image/gif'
        )
        form_data = {
            'first_name': 'Другое имя',
            'last_name': 'Другая фамилия',
            'email': 'test@test.ru',
            'city': 'Екатеринбург',
            'vk': 'newuser',
            'telegram': 'newuser',
            'instagram': 'newuser',
            'git': 'newuser',
            'profile_pic': image,
        }
        response = self.authorized_client.post(
            reverse('users:change'),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse(
            'posts:profile', args=(self.user.username,)),
            HTTPStatus.FOUND
        )
        user = User.objects.first()
        check_edited_profile_fields = (
            (user.city, user.city),
            (user.vk, user.vk),
            (user.telegram, user.telegram),
            (user.instagram, user.instagram),
            (user.git, user.git),
            (user.profile_pic, f'users/{image}'),
        )
        for new_data, expected in check_edited_profile_fields:
            with self.subTest(new_post=expected):
                self.assertEqual(new_data, expected)
        user = User.objects.first()
        check_edited_profile_fields = (
            (user.first_name, user.first_name),
            (user.last_name, user.last_name),
            (user.email, user.email),
        )
        for new_data, expected in check_edited_profile_fields:
            with self.subTest(new_post=expected):
                self.assertEqual(new_data, expected)
        self.assertEqual(User.objects.count(), 1)

    def test_register_form(self):
        """Проверка формы регистрации."""
        form_data = {
            'username': 'username',
            'first_name': 'Новое имя',
            'last_name': 'новая фамилия',
            'email': 'test@test.ru',
            'password1': '123TGWp76',
            'password2': '123TGWp76',
        }
        response = self.authorized_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse(
            'posts:index'),
            HTTPStatus.FOUND
        )
        user = User.objects.get(pk=2)
        check_edited_profile_fields = (
            (user.username, user.username),
            (user.first_name, user.first_name),
            (user.last_name, user.last_name),
            (user.email, user.email),
        )
        for new_data, expected in check_edited_profile_fields:
            with self.subTest(new_post=expected):
                self.assertEqual(new_data, expected)
        self.assertEqual(User.objects.count(), 2)
