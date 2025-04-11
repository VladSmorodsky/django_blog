from django.conf import settings
from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth.models import User
from django.db import models
from django.urls.base import reverse
from django.utils import timezone
from tinymce.models import HTMLField


class PublishedManager(models.Manager):
    """
    Manager works with published posts
    """

    def get_queryset(self) -> models.QuerySet:
        """
        Return only published posts
        :return:
        """
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Create your models here.
class UserProfile(models.Model):
    """
    User profile model
    """
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}"


class Category(models.Model):
    """
    Category model
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Post(models.Model):
    class Status(models.TextChoices):
        """
        Represents post status
        """
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=100)
    content = HTMLField()
    slug = models.SlugField(max_length=100, unique_for_date='published_at')
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='blog_posts')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
        ]

    def get_absolute_url(self) -> str:
        """
        Return absolute url
        :return:
        """
        return reverse('post_detail', args=[self.slug])

    def __str__(self) -> str:
        return f"{self.title}"


class Comment(models.Model):
    """
    Comment model
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self) -> str:
        return f"Comment by {self.author} on {self.post}"
