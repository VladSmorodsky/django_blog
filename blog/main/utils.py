from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http.request import HttpRequest

from main.models import Post


def send_register_email(request: HttpRequest, user: User) -> None:
    """
    Sending email about user successful registration
    :param request:
    :param user:
    :return:
    """
    subject = f"Welcome to Django Blog, {user.username}!"
    content = f"You successfully registered on {request.build_absolute_uri('/')}! You can read posts and write comments. Have fun!"
    send_mail(subject, content, settings.EMAIL_HOST_USER, [user.email])


def send_published_comment_email(request: HttpRequest, post: Post) -> None:
    """
    Sending to post's author email about published comment
    :param request:
    :param post:
    :return:
    """
    subject = f"Added comment to post {post.title}!"
    content = f"Dear {post.author.username}! New comment was added to you post: {post.title}!"
    send_mail(subject, content, settings.EMAIL_HOST_USER, [post.author.email])
