from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Author')
        cls.user_no_author = User.objects.create_user(username='NoAuthor')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая запись',
            group=cls.group,
        )
        cls.urls = (
            ('posts:index', None, 'posts/index.html', '/'),
            ('posts:profile', (cls.user,), 'posts/profile.html',
             f'/profile/{cls.user.username}/'),
            ('posts:group_list', (cls.group.slug,), 'posts/group_list.html',
             f'/group/{cls.group.slug}/'),
            ('posts:post_detail', (cls.post.id,), 'posts/post_detail.html',
             f'/posts/{cls.post.id}/'),
            ('posts:post_create', None, 'posts/create_post.html', '/create/'),
            ('posts:post_edit', (cls.post.id,), 'posts/create_post.html',
             f'/posts/{cls.post.id}/edit/'),
            ('posts:post_delete', (cls.post.id,), None,
             f'/posts/{cls.post.id}/delete/'),
            ('posts:follow_index', None, 'posts/follow.html', '/follow/'),
            ('posts:profile_follow', (cls.user,), None,
             f'/profile/{cls.user.username}/follow/'),
            ('posts:profile_unfollow', (cls.user,), None,
             f'/profile/{cls.user.username}/unfollow/'),
            ('posts:add_comment', (cls.post.id,), None,
             f'/posts/{cls.post.id}/comment/'),
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_no_author = Client()
        self.authorized_client_no_author.force_login(self.user_no_author)
        cache.clear()

    def test_reverse(self):
        """Проверка реверсов."""
        for url, args, _, hard_link in self.urls:
            reverse_name = reverse(url, args=args)
            with self.subTest(reverse_name=hard_link):
                self.assertEqual(reverse_name, hard_link)

    def test_urls_exists_at_desired_location_for_author(self):
        """Проверка доступности адресов страниц для автора."""
        redirect_to_profile = (
            'posts:post_delete',
            'posts:profile_follow',
            'posts:profile_unfollow',
        )
        redirect_to_post_detail = (
            'posts:add_comment',
        )
        for url, args, _, _ in self.urls:
            reverse_name = reverse(url, args=args)
            with self.subTest(reverse_name=reverse_name):
                if url in redirect_to_profile:
                    response = self.authorized_client.get(
                        reverse_name, follow=True
                    )
                    redirect = reverse('posts:profile', args=(self.user,))
                    self.assertRedirects(response, redirect, HTTPStatus.FOUND)
                elif url in redirect_to_post_detail:
                    response = self.authorized_client.get(
                        reverse_name, follow=True
                    )
                    redirect = reverse('posts:post_detail', args=args)
                else:
                    response = self.authorized_client.get(
                        reverse_name
                    )
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_exists_at_desired_location_for_user(self):
        """Проверка доступности адресов страниц для пользователя."""
        redirect_to_profile = (
            'posts:profile_follow',
            'posts:profile_unfollow',
        )
        redirect_to_post_detail = (
            'posts:post_delete',
            'posts:post_edit',
            'posts:add_comment',
        )
        for url, args, _, _ in self.urls:
            reverse_name = reverse(url, args=args)
            with self.subTest(reverse_name=reverse_name):
                if url in redirect_to_profile:
                    response = self.authorized_client_no_author.get(
                        reverse_name, follow=True
                    )
                    redirect = reverse('posts:profile', args=(self.user,))
                    self.assertRedirects(response, redirect, HTTPStatus.FOUND)
                elif url in redirect_to_post_detail:
                    response = self.authorized_client_no_author.get(
                        reverse_name, follow=True
                    )
                    redirect = reverse('posts:post_detail', args=args)
                    self.assertRedirects(response, redirect, HTTPStatus.FOUND)
                else:
                    response = self.authorized_client_no_author.get(
                        reverse_name
                    )
                    self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_exists_at_desired_location_for_guest(self):
        """Проверка доступности адресов страниц для гостя."""
        rederict_urls = (
            'posts:post_create',
            'posts:post_edit',
            'posts:post_delete',
            'posts:follow_index',
            'posts:profile_follow',
            'posts:profile_unfollow',
            'posts:add_comment',
        )
        for url, args, _, _ in self.urls:
            reverse_name = reverse(url, args=args)
            with self.subTest(reverse_name=reverse_name):
                if url in rederict_urls:
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

    def test_urls_uses_correct_template_for_author(self):
        """Проверка использования шаблонов страниц."""
        without_template = (
            'posts:post_delete',
            'posts:profile_follow',
            'posts:profile_unfollow',
            'posts:add_comment',
        )
        for url, args, template, _ in self.urls:
            reverse_name = reverse(url, args=args)
            with self.subTest(reverse_name=reverse_name):
                if url in without_template:
                    continue
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_404_nonexistent_page(self):
        """Проверка 404 для несуществующих страниц."""
        url = '/unexisting_page/'
        roles = (
            self.authorized_client,
            self.authorized_client_no_author,
            self.client,
        )
        for role in roles:
            with self.subTest(url=url):
                response = role.get(url, follow=True)
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
                self.assertTemplateUsed(response, 'core/404.html')
