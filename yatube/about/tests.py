from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class StaticPagesURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.urls = (
            ('about:author', '/about/author/', 'about/author.html'),
            ('about:tech', '/about/tech/', 'about/tech.html'),
        )

    def test_reverse(self):
        """Проверка реверсов."""
        for url, hard_link, _ in self.urls:
            reverse_name = reverse(url)
            with self.subTest(reverse_name=hard_link):
                self.assertEqual(reverse_name, hard_link)

    def test_static_url_exists_at_desired_location(self):
        """Проверка доступности адреса статичных страниц."""
        for url, _, _ in self.urls:
            reverse_name = reverse(url)
            with self.subTest(reverse_name):
                response = self.client.get(reverse_name)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_static_url_uses_correct_template(self):
        """Проверка шаблонов статичных страниц."""
        for url, _, template in self.urls:
            reverse_name = reverse(url)
            with self.subTest(reverse_name):
                response = self.client.get(reverse_name)
                self.assertTemplateUsed(response, template)
