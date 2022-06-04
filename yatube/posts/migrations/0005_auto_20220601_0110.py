# Generated by Django 2.2.16 on 2022-05-31 20:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0004_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, help_text='Добавить картинку', upload_to='posts/', verbose_name='Картинка'),
        ),
        migrations.CreateModel(
            name='CommentForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Текст комментария', verbose_name='Текст комментария')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='posts.Post', verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'комментарии',
            },
        ),
    ]
