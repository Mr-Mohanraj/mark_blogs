from django.db import models
from authentication.models import User


class Post(models.Model):
    title = models.CharField(max_length=1000)
    body = models.TextField(default="There no body")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="likes", default=0)
    dislikes = models.ManyToManyField(
        User, blank=True, related_name="dislikes", default=0)

    class Meta:
        ordering = ["-create_at"]

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:blog_detail', args=[self.pk])
