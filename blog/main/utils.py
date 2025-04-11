from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http.request import HttpRequest


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
