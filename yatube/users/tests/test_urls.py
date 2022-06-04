from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class UsersURLTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Username')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_open_urls_exists_at_desired_location(self):
        """Проверка доступности адресов открытых страниц для гостя."""
        urls = (
            '/auth/login/',
            '/auth/signup/',
            '/auth/password_reset/',
            '/auth/reset/done/',
            '/auth/reset/<uidb64>/<token>/',
            '/auth/logout/',
        )
        for urls in urls:
            with self.subTest(urls=urls):
                response = self.client.get(urls)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_open_urls_uses_correct_template(self):
        """Проверка использования шаблонов открытых страниц."""
        template_url_names = {
            'users/login.html': '/auth/login/',
            'users/signup.html': '/auth/signup/',
            'users/password_reset_form.html': '/auth/password_reset/',
            'users/password_reset_complete.html': '/auth/reset/done/',
            'users/password_reset_confirm.html':
            '/auth/reset/<uidb64>/<token>/',
            'users/logged_out.html': '/auth/logout/',
        }
        for template, urls in template_url_names.items():
            with self.subTest(urls=urls):
                response = self.client.get(urls)
                self.assertTemplateUsed(response, template)

    def test_close_urls_exists_at_desired_location(self):
        """Проверка доступности адресов для пользователя."""
        urls = (
            '/auth/password_change/',
            '/auth/password_change/done/',
        )
        for urls in urls:
            with self.subTest(urls=urls):
                response = self.authorized_client.get(urls)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_close_urls_uses_correct_template(self):
        """Проверка шаблонов для пользователя."""
        template_url_names = {
            'users/password_change_form.html': '/auth/password_change/',
            'users/password_change_done.html': '/auth/password_change/done/',
        }
        for template, urls in template_url_names.items():
            with self.subTest(urls=urls):
                response = self.authorized_client.get(urls)
                self.assertTemplateUsed(response, template)
