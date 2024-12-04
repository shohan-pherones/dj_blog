from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm
from .models import Post
from .forms import PostForm, CommentForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse


def index(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'blog/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
def user_profile(request):
    user_posts = Post.objects.filter(
        author=request.user).order_by('-created_at')
    return render(request, 'blog/user_profile.html', {'user_posts': user_posts})


def create_post(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        raise Http404("You are not allowed to edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        raise Http404("You are not allowed to delete this post.")

    post.delete()
    return redirect('index')


@login_required
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            post.dislikes.remove(request.user)
            liked = True
        return JsonResponse({'liked': liked, 'likes_count': post.total_likes()})
    return HttpResponse(status=405)


@login_required
def dislike_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.dislikes.all():
            post.dislikes.remove(request.user)
            disliked = False
        else:
            post.dislikes.add(request.user)
            post.likes.remove(request.user)
            disliked = True
        return JsonResponse({'disliked': disliked, 'dislikes_count': post.total_dislikes()})
    return HttpResponse(status=405)
