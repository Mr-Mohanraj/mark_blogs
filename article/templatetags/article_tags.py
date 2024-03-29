from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post, User


register = template.Library()


@register.simple_tag
def total_posts(user_id):
    return Post.objects.filter(author=user_id).count()


@register.inclusion_tag('article/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.order_by('-created')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.objects.annotate(
               total_comments=Count('comments')
           ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
