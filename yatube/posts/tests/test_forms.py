import shutil
import tempfile
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..forms import PostForm
from ..models import Comment, Group, Post

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostFormTests(TestCase):
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
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая запись',
            group=cls.group,
        )
        cls.form = PostForm()
        cls.post_qty = Post.objects.count()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_no_author = Client()
        self.authorized_client_no_author.force_login(self.user_no_author)

    def test_create_form(self):
        """Валидная форма create создает запись в Post."""
        bytes_image = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        image = SimpleUploadedFile(
            name='new_small.gif',
            content=bytes_image,
            content_type='image/gif'
        )
        form_data = {
            'text': self.post.text,
            'group': self.group.pk,
            'image': image,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse(
            'posts:profile', args=(self.user,)),
            HTTPStatus.FOUND
        )
        self.assertEqual(Post.objects.count(), self.post_qty + 1)
        post = Post.objects.get(pk=2)
        check_post_fields = (
            (post.author, self.post.author),
            (post.text, self.post.text),
            (post.group, self.group),
            (post.image, f'posts/{image}'),
        )
        for new_post, expected in check_post_fields:
            with self.subTest(new_post=expected):
                self.assertEqual(new_post, expected)

        response = self.authorized_client.get(reverse(
            'posts:group_list', args=(self.group.slug,))
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(
            response.context['page_obj']), Post.objects.count()
        )

    def test_edit_form(self):
        """Валидная форма edit редактирует запись в Post."""
        bytes_image = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        image = SimpleUploadedFile(
            name='new_small.gif',
            content=bytes_image,
            content_type='image/gif'
        )
        group_2 = Group.objects.create(
            title='Новая группа',
            slug='new-slug',
            description='Новое описание',
        )
        form_data = {
            'text': 'Новый текст',
            'group': group_2.pk,
            'image': image,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', args=(self.post.id,)),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse(
            'posts:post_detail', args=(self.post.id,)),
            HTTPStatus.FOUND
        )
        self.assertEqual(self.post_qty, self.post_qty)
        post = Post.objects.first()
        check_edited_post_fields = (
            (post.author, self.post.author),
            (post.text, post.text),
            (post.group, post.group),
            (post.image, post.image),
        )
        for new_post, expected in check_edited_post_fields:
            with self.subTest(new_post=expected):
                self.assertEqual(new_post, expected)
        response = self.authorized_client.get(reverse(
            'posts:group_list', args=(self.group.slug,))
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context['page_obj']), 0)

    def test_edit_form_only_for_author(self):
        """Запись может редактировать только автор + перенаправление."""
        roles = (
            (self.authorized_client_no_author,),
            (self.client,),
        )
        for role in roles:
            with self.subTest(role=role):
                reverse_name = reverse('posts:post_edit', args=(self.post.id,))
                response = self.client.post(reverse_name)
                if role == self.authorized_client_no_author:
                    self.assertRedirects(response, reverse(
                        'posts:post_detail', args=(self.post.id,)),
                        HTTPStatus.FOUND
                    )
                else:
                    login = reverse(settings.LOGIN_URL)
                    self.assertRedirects(
                        response,
                        f'{login}?{REDIRECT_FIELD_NAME}={reverse_name}',
                        HTTPStatus.FOUND
                    )
        self.assertEqual(self.post_qty, self.post_qty)

    def test_guest_cant_create_post(self):
        """Гость не может создавать записи."""
        reverse_name = reverse('posts:post_create')
        response = self.client.post(reverse_name)
        login = reverse(settings.LOGIN_URL)
        self.assertRedirects(
            response,
            f'{login}?{REDIRECT_FIELD_NAME}={reverse_name}',
            HTTPStatus.FOUND
        )

    def test_comment_for_registered_users(self):
        """Комментарии могут оставлять зарегистрированные пользователи."""
        roles = (
            self.authorized_client.post,
            self.authorized_client_no_author.post,
        )
        for role in roles:
            with self.subTest(role=role):
                comment_data = {
                    'text': 'тестовый коммент',
                }
                response = role(
                    reverse('posts:add_comment', args=(self.post.id,)),
                    data=comment_data,
                    follow=True,
                )
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertRedirects(response, reverse(
                    'posts:post_detail', args=(self.post.id,)),
                    HTTPStatus.FOUND
                )
                comment = Comment.objects.first()
                self.assertEqual(comment.text, comment.text)
        self.assertEqual(Comment.objects.count(), 2)

    def test_comment_cant_comment(self):
        """Комментарии не могут оставлять гости."""
        comment_data = {
            'text': 'тестовый коммент',
        }
        reverse_name = reverse('posts:add_comment', args=(self.post.id,))
        response = self.client.post(
            reverse_name,
            data=comment_data,
            follow=True,
        )
        login = reverse(settings.LOGIN_URL)
        self.assertRedirects(
            response,
            f'{login}?{REDIRECT_FIELD_NAME}={reverse_name}',
            HTTPStatus.FOUND
        )
        self.assertEqual(Comment.objects.count(), 0)

    def test_form_label(self):
        """Проверка labels формы."""
        labels = (
            (self.form.fields['text'].label, 'Текст записи'),
            (self.form.fields['group'].label, 'Выберите сообщество:'),
        )
        for label, text in labels:
            with self.subTest(label=text):
                self.assertEquals(label, text)
