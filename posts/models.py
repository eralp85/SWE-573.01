from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    link = models.CharField(max_length=200, null='True', blank='True', unique='False')
    tags = models.CharField(max_length=200, blank=True)
    labels = models.CharField(max_length=200, blank=True)
    text = models.CharField(max_length=2000, blank=True)
    upload = models.FileField(upload_to='uploads/', null='True', blank='True', unique='False')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title



class Author(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=15, null=True,blank=True)
    email = models.CharField(max_length=50, null=True)
    profile_pic = models.ImageField(default="blank-profile-photo.jpeg", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user

    def approve(self):
        self.approved_comment = True
        self.save()



class Comment(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.OneToOneRel(field_name='author_id', to='Author.id', field= 'none',  on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
