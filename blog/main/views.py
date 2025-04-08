from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView

from main.models import Post


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
    return render(request, 'main/post/detail.html', {'post': post})
