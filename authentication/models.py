from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

"""“Following” is the term for the users who you follow. "Followers" are the users who follow you."""


class User(AbstractUser):
    modified_at = models.DateTimeField(auto_now=True)
    total_post = models.PositiveIntegerField(default=0)
    followers = models.ManyToManyField(
        "self", blank=True, related_name="follower", symmetrical=False)
    followings = models.ManyToManyField(
        "self", blank=True, related_name="following", symmetrical=False
    )


    def __str__(self):
        return str(self.username)

    def get_post_count(self):
        return self.total_post

    def get_absolute_url(self):
        return reverse('blog:profile', kwargs={'pk': self.pk})


class Token(models.Model):
    activation_token = models.CharField(max_length=64)
    reset_token = models.CharField(max_length=64)
