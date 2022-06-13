from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm, UserUpdateForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


@login_required
def change(request):
    """Функция редактирования профиля."""
    if request.method == 'POST':
        form = UserUpdateForm(
            request.POST,
            files=request.FILES or None,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect('posts:profile', request.user.username)
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'users/change.html', {'form': form})
