from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.contrib import messages

from main.forms import LoginForm, RegisterForm, CommentForm
from main.models import Post, UserProfile, Comment
from main.utils import send_register_email, send_published_comment_email


# Create your views here.

class PostListView(ListView):
    """
    View to list all published posts
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'main/post/list.html'


def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Get post details
    :param slug:
    :param request:
    :return:
    """
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
    comments = Comment.objects.filter(post=post)
    return render(request, 'main/post/detail.html', {'post': post, 'comments': comments})


def login_view(request: HttpRequest) -> HttpResponse:
    """
    Login view
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return redirect('post_list')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = authenticate(request=request, username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, "You are now logged in")
                        return redirect("post_list")
                else:
                    messages.error(request, "Invalid username or password")
            except AttributeError:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'main/account/auth_page.html', {'form': form, 'auth_form_action': 'Login'})


def register_view(request: HttpRequest) -> HttpResponse:
    """
    Register a new user
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return redirect("post_list")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            send_register_email(request, user)
            return redirect('post_list')
    else:
        form = RegisterForm()
    return render(request, 'main/account/auth_page.html', {'form': form, 'auth_form_action': 'Register'})


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Logout a user
    :param request:
    :return:
    """
    logout(request)
    return redirect("login")


@login_required
def add_comment_view(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Add comment to post
    :param request:
    :param slug:
    :return:
    """
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            send_published_comment_email(request, post)
            messages.success(request, "Your comment added!")
            return redirect("post_detail", post.slug)
    else:
        form = CommentForm()
    return render(request, 'main/comment/add_comment.html', {'form': form})
