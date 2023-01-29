from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    join_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    total_post = models.PositiveIntegerField(default=0)
    is_login = models.BooleanField(default=False)

    def get_post_count(self):
        return self.total_post


class Post(models.Model):
    title = models.CharField(max_length=1000)
    body = models.TextField(default="There no body")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, models.CASCADE)
    
    class Meta:
        ordering = ["-create_at"]
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:blog_detail', args=[self.pk])

class Token(models.Model):
    activation_token = models.CharField(max_length=64)
    reset_token = models.CharField(max_length=64)