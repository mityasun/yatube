# Generated by Django 2.2.16 on 2022-06-13 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220613_1758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
    ]