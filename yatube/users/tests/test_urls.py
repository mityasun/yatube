from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UsersURLTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Username')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.urls = (
            ('users:signup', '/auth/signup/', 'users/signup.html'),
            ('users:login', '/auth/login/', 'users/login.html'),
            ('users:change', '/auth/change/', 'users/change.html'),
            ('users:password_change',
             '/auth/password_change/',
             'users/password_change_form.html'),
            ('users:password_change_done',
             '/auth/password_change/done/',
             'users/password_change_done.html'),
            ('users:password_reset',
             '/auth/password_reset/',
             'users/password_reset_form.html'),
            ('users:password_reset_done',
             '/auth/password_reset/done/',
             'users/password_reset_done.html'),
            ('users:password_reset_complete',
             '/auth/reset/done/',
             'users/password_reset_complete.html'),
            ('users:logout', '/auth/logout/', 'users/logged_out.html'),

        )

    def test_reverse(self):
        """Проверка реверсов."""
        for url, hard_link, _ in self.urls:
            reverse_name = reverse(url)
            with self.subTest(reverse_name=hard_link):
                self.assertEqual(reverse_name, hard_link)

    def test_open_urls_exists_at_desired_location(self):
        """Проверка доступности адресов открытых страниц для гостя."""
        close_urls = (
            'users:password_change',
            'users:password_change_done',
            'users:profile',
            'users:change',
            '/auth/logout/',
        )
        for url, _, _ in self.urls:
            reverse_name = reverse(url)
            with self.subTest(url=url):
                if url in close_urls:
                    response = self.client.get(reverse_name, follow=True)
                    login = reverse(settings.LOGIN_URL)
                    self.assertRedirects(
                        response,
                        f'{login}?{REDIRECT_FIELD_NAME}={reverse_name}',
                        HTTPStatus.FOUND
                    )
                else:
                    response = self.client.get(reverse_name)
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_close_urls_exists_at_desired_location(self):
        """Проверка доступности адресов для пользователя."""
        for url, _, _ in self.urls:
            reverse_name = reverse(url)
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """Проверка шаблонов."""
        for url, _, template in self.urls:
            reverse_name = reverse(url)
            with self.subTest(url=url):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
