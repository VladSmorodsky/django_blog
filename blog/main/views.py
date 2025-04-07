from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from main.models import Post


# Create your views here.

def post_list(request: HttpRequest) -> HttpResponse:
    """
    Get all published posts
    :param request:
    :return:
    """
    posts = Post.published.all()
    return render(request, 'main/post/list.html', {'posts': posts})


def post_detail(request: HttpRequest, id: int) -> HttpResponse:
    """
    Get post details
    :param request:
    :param id:
    :return:
    """
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    return render(request, 'main/post/detail.html', {'post': post})
