from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, LoginForm
from .models import Post
from .forms import PostForm


def index(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})


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
    post = Post.objects.get(id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})


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
