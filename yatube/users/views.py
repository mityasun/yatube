from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CreationForm, UserUpdateForm


def register(request):
    """Функция создания пользователя."""

    form = CreationForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.save()
        form.cleaned_data.get('username')
        new_user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )
        login(request, new_user)
        return redirect('posts:index')
    else:
        form = CreationForm()
    return render(request, 'users/signup.html', {'form': form})


@login_required
def change(request):
    """Функция редактирования пользователя."""

    form = UserUpdateForm(
        request.POST or None,
        files=request.FILES or None,
        instance=request.user
    )
    if form.is_valid():
        form.save()
        return redirect('posts:profile', request.user.username)
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/change.html', {'form': form})
