from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class CreationForm(UserCreationForm):
    class Meta:
        model = User

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Ваше ник'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ваша фамилия'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ваш e-mail'}),
            'city': forms.TextInput(attrs={'placeholder': 'Ваш город'}),
            'vk': forms.TextInput(attrs={'placeholder': 'Ваш ник Вконтакте'}),
            'telegram': forms.TextInput(
                attrs={'placeholder': 'Ваш ник в Telegram'}
            ),
            'instagram': forms.TextInput(
                attrs={'placeholder': 'Ваш ник в Instagram'}
            ),
            'git': forms.TextInput(attrs={'placeholder': 'Ваш ник на github'}),
        }

        fields = (
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'email',
            'profile_pic',
            'city',
            'vk',
            'telegram',
            'instagram',
            'git'
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Ваша фамилия'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ваш e-mail'}),
            'city': forms.TextInput(attrs={'placeholder': 'Ваш город'}),
            'vk': forms.TextInput(attrs={'placeholder': 'Ваш ник Вконтакте'}),
            'telegram': forms.TextInput(
                attrs={'placeholder': 'Ваш ник в Telegram'}
            ),
            'instagram': forms.TextInput(
                attrs={'placeholder': 'Ваш ник в Instagram'}
            ),
            'git': forms.TextInput(attrs={'placeholder': 'Ваш ник на github'}),
        }

        fields = (
            'first_name',
            'last_name',
            'email',
            'profile_pic',
            'city',
            'vk',
            'telegram',
            'instagram',
            'git'
        )
