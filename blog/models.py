from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class User(AbstractUser):
    join_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    total_post = models.PositiveIntegerField(default=0)
    is_login = models.BooleanField(default=False)
    
    def get_post_count(self):
        return self.total_post
    
    def get_absolute_url(self):
        return reverse('blog:profile', kwargs={'pk': self.pk})


class Post(models.Model):
    title = models.CharField(max_length=1000)
    body = models.TextField(default="There no body")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    dislikes = models.ManyToManyField(User, blank=True, related_name="dislikes")

    class Meta:
        ordering = ["-create_at"]

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:blog_detail', args=[self.pk])


class Token(models.Model):
    activation_token = models.CharField(max_length=64)
    reset_token = models.CharField(max_length=64)

class Follower(models.Model):
    follower = models.ManyToManyField(User,related_name="follower")
    following = models.ManyToManyField(User, related_name="following")
    followers_count = models.PositiveBigIntegerField(default=0)
    following_count = models.PositiveBigIntegerField(default=0)