from typing import Any
from django.urls import reverse
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.contrib.auth import get_user_model
from authenticator.models import Profile

# Create your models here.


class Post(models.Model):
    # STATUS_CHOICES = (
    #     ('draft', 'Draft'),
    #     ('published', 'Published'),
    # )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    link = models.CharField(max_length=200, null=True, blank=True, unique=False)
    tags = TaggableManager()
    labels = models.CharField(max_length=200, blank=True)
    text = models.CharField(max_length=2000, blank=True)
    upload = models.FileField(upload_to='uploads/', null=True, blank=True, unique=False)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='blog_post')
    title_tag = models.CharField(max_length=200, null=True, blank=True, unique=False)
    # status = models.CharField(max_length=10,
    #                           choices=STATUS_CHOICES,
    #                           default='draft')

    def total_likes(self):
        return self.likes.count()


    class Meta:
        ordering = ('-published_date',)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[self.id])


class Comment(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.OneToOneRel(field_name='author_id', to='Author.id', field='none',  on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)


    class Meta:
        ordering = ('created_date',)
        indexes = [
            models.Index(fields=['created_date']),]


    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
        return f'Comment by {self.name} on {self.post}'


class Contact(models.Model):
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


# Add following field to User dynamically
user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField('self',
                                                through=Contact,
                                                related_name='followers',
                                                symmetrical=False))