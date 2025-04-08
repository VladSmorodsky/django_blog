from django.conf import settings
from django.db import models
from django.urls.base import reverse
from django.utils import timezone


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

class Post(models.Model):
    class Status(models.TextChoices):
        """
        Represents post status
        """
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=100)
    content = models.TextField()
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
