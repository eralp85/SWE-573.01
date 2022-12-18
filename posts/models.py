from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth. models import User

# Create your models here.


class Label(models.Model):
    CATEGORY = (
        ('Macro Economy', 'Macro Economy'),
        ('Equity', 'Equity'),
        ('Fixed Income', 'Fixed Income'),
        ('Company News', 'Company News')
    )

    label = models.CharField(max_length=200, null=True, choices=CATEGORY)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.label
class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    link = models.CharField(max_length=200, null='True', blank='True', unique='False')
    tags = models.ManyToManyField(Tag, blank=True)
    labels = models.ManyToManyField(Label, blank=True)
    text = models.TextField(blank=True)
    upload = models.FileField(upload_to='uploads/', null='True', blank='True', unique='False')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)


    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text





class Author(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
