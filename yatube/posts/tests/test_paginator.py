from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.paginator import Paginator
from django.test import TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PaginatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post_qty = 99
        Post.objects.bulk_create(
            [Post(
                author=cls.user,
                text=f'Тестовая запись{post}',
                group=cls.group
            )for post in range(cls.post_qty)]
        )
        cls.urls = (
            ('posts:index', None),
            ('posts:profile', (cls.user,)),
            ('posts:group_list', (cls.group.slug,)),
        )

    def test_paginator_correct(self):
        """Пагинатор работает корректно."""
        paginator = Paginator(Post.objects.all(), settings.LIMIT_POSTS)
        for url, args in self.urls:
            reverse_name = reverse(url, args=args)
            with self.subTest(reverse_name=reverse_name):
                for page in paginator.page_range:
                    if page < paginator.num_pages:
                        number_page = f'{reverse_name}?page={page}'
                        response = self.client.get(number_page)
                        self.assertEqual(
                            len(response.context['page_obj']),
                            settings.LIMIT_POSTS
                        )
                    end_page = f'{reverse_name}?page={paginator.num_pages}'
                    cache.clear()
                    response = self.client.get(end_page)
                    self.assertEqual(
                        len(response.context['page_obj']),
                        paginator.count - settings.LIMIT_POSTS
                        * (paginator.num_pages - 1)
                    )
