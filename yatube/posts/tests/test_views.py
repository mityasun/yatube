import shutil
import tempfile
from http import HTTPStatus

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..forms import PostForm
from ..models import Follow, Group, Post

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='Author')
        cls.user_no_author = User.objects.create_user(username='NoAuthor')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.bytes_image = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.image = SimpleUploadedFile(
            name='small.gif',
            content=cls.bytes_image,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая запись',
            group=cls.group,
            image=cls.image
        )
        cls.post_qty = Post.objects.count()
        cls.urls = (
            ('posts:index', None, 'posts/index.html'),
            ('posts:profile', (cls.user,), 'posts/profile.html'),
            ('posts:group_list', (cls.group.slug,), 'posts/group_list.html'),
            ('posts:post_detail', (cls.post.id,), 'posts/post_detail.html'),
            ('posts:post_create', None, 'posts/create_post.html'),
            ('posts:post_edit', (cls.post.id,), 'posts/create_post.html'),
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_no_author = Client()
        self.authorized_client_no_author.force_login(self.user_no_author)
        cache.clear()

    def test_pages_uses_correct_template(self):
        """view-функции использует соответствующий шаблон."""
        for url, args, template in self.urls:
            reverse_name = reverse(url, args=args)
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def check_context(self, response, bool=False):
        """Функция для передачи контекста."""
        if bool:
            post = response.context.get('post')
        else:
            post = response.context['page_obj'][0]
        self.assertEqual(post.text, self.post.text)
        self.assertEqual(post.pub_date, self.post.pub_date)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.group, self.group)
        self.assertEqual(post.image, f'posts/{self.image}')

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        self.check_context(response)
        self.assertContains(response, '<img', count=2)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', args=(self.user,))
        )
        self.check_context(response)
        self.assertEqual(response.context.get('author'), self.user)
        self.assertContains(response, '<img', count=2)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', args=(self.group.slug,))
        )
        self.check_context(response)
        self.assertEqual(response.context.get('group'), self.group)
        self.assertContains(response, '<img', count=2)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', args=(self.post.id,))
        )
        self.check_context(response, True)
        self.assertContains(response, '<img', count=2)

    def test_create_edit_page_show_correct_form(self):
        """post_create и post_edit сформированы с правильным контекстом."""
        urls = (
            ('posts:post_create', None),
            ('posts:post_edit', (self.post.id,)),
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ChoiceField,
        }
        for url, slug in urls:
            reverse_name = reverse(url, args=slug)
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                for value, expected in form_fields.items():
                    with self.subTest(value=value):
                        form_field = response.context.get('form').fields.get(
                            value
                        )
                        self.assertIsInstance(form_field, expected)
                        self.assertIsInstance(response.context['form'],
                                              PostForm)

    def test_post_appears_at_group(self):
        """Пост НЕ появляется в другой группе."""
        Post.objects.create(
            author=self.user,
            text='Текстовый текст',
            group=self.group
        )
        group_2 = Group.objects.create(
            title='Тестовая группа 2',
            slug='test-group-2',
            description='Тестовое описание 2',
        )
        response = self.authorized_client.get(
            reverse('posts:group_list', args=(group_2.slug,))
        )
        self.assertEqual(len(response.context['page_obj']), 0)

    def test_post_delete(self):
        """Проверка удаления поста."""
        post = Post.objects.create(
            author=self.user,
            text='Пост для проверки функции удаления',
            group=self.group
        )
        id_post = post.id
        response = self.authorized_client.get(
            reverse('posts:post_delete', args=(post.id,))
        )
        rederict = reverse('posts:profile', args=(self.user,))
        self.assertRedirects(response, rederict, HTTPStatus.FOUND)
        self.assertFalse(Post.objects.filter(pk=id_post).exists())
        self.assertEqual(Post.objects.count(), self.post_qty)
        response = self.authorized_client.get(reverse(
            'posts:group_list', args=(self.group.slug,))
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(
            response.context['page_obj']), self.post_qty
        )

    def test_cache(self):
        """Проверка работы кэша."""
        post = Post.objects.create(
            author=self.user,
            text='Пост для провери кэша',
            group=self.group
        )
        response_1 = self.client.get(reverse('posts:index'))
        self.assertTrue(Post.objects.get(pk=post.id))
        Post.objects.get(pk=post.id).delete()
        response_2 = self.client.get(reverse('posts:index'))
        self.assertEqual(response_1.content, response_2.content)
        cache.clear()
        response_3 = self.client.get(reverse('posts:index'))
        self.assertNotEqual(response_1.content, response_3.content)

    def test_users_can_follow_and_unfollow(self):
        """Зарегистрированный пользователь может подписаться и отписаться."""
        follower_qty = Follow.objects.count()
        response = self.authorized_client_no_author.get(
            reverse('posts:profile_follow', args=(self.user,))
        )
        self.assertRedirects(
            response, reverse('posts:profile', args=(self.user,)),
            HTTPStatus.FOUND
        )
        self.assertEqual(Follow.objects.count(), follower_qty + 1)
        response = self.authorized_client_no_author.get(
            reverse('posts:profile_unfollow', args=(self.user,))
        )
        self.assertRedirects(
            response, reverse('posts:profile', args=(self.user,)),
            HTTPStatus.FOUND
        )
        self.assertEqual(Follow.objects.count(), follower_qty)

    def test_post_appears_at_feed(self):
        """Пост появляется в лента подписчика."""
        Follow.objects.get_or_create(
            user=self.user_no_author,
            author=self.user
        )
        response = self.authorized_client_no_author.get(
            reverse('posts:follow_index')
        )
        self.assertContains(response, self.post)
        Follow.objects.filter(
            user=self.user_no_author,
            author__username=self.user.username
        ).delete()
        response = self.authorized_client_no_author.get(
            reverse('posts:follow_index')
        )
        self.assertNotContains(response, self.post)
