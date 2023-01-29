from django import template
from ..models import Post
from django.db.models import Count


register = template.Library()


@register.simple_tag
def total_posts():

    return Post.objects.filter()


@register.inclusion_tag('posts/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.order_by('-published_date')[:count]
    return {'latest_posts': latest_posts}


