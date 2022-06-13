from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post
from .utils import paginator

User = get_user_model()


def index(request):
    """Главная страница с записями."""
    posts = Post.objects.select_related('author', 'group')
    context = {
        'page_obj': paginator(posts, request),
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Страница сообществ с записями."""
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author')
    context = {
        'group': group,
        'page_obj': paginator(posts, request),
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Страница автора с его записями."""
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('group')
    following = Follow.objects.filter(
        user=request.user.id, author__following__author=author)
    context = {
        'author': author,
        'following': following,
        'page_obj': paginator(posts, request),
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Страница одной записи."""
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.select_related('author')
    form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required()
def post_create(request):
    """Функция создания записи."""
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author.username)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    """Функция редактирования записи."""
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_delete(request, post_id):
    """Функция удаления записи."""
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    post.delete()
    return redirect('posts:profile', post.author.username)


@login_required
def add_comment(request, post_id):
    """Функция создания комментариев."""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id)


@login_required
def follow_index(request):
    """Функция страницы с подписками."""
    posts = Post.objects.select_related('author', 'group').filter(
        author__following__user=request.user)
    context = {
        'page_obj': paginator(posts, request),
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    """Функция подписки на автора."""
    author = get_object_or_404(User, username=username)
    follower = request.user
    if follower != author and follower != author.follower:
        Follow.objects.get_or_create(user=follower, author=author)
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    """Функция отписки от автора."""
    Follow.objects.filter(
        user=request.user,
        author__username=username
    ).delete()
    return redirect('posts:profile', username)
