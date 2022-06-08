from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class CreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Ваша фамилия'}
            ),
            'email': forms.TextInput(attrs={'placeholder': 'Ваш e-mail'}),
        }
        fields = ('first_name', 'last_name', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile

        widgets = {
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
        fields = ('profile_pic', 'city', 'vk', 'telegram', 'instagram', 'git')
