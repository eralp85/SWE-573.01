from django.contrib import admin
from .models import Post,Comment,Author,Tag,Label

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Label)

# Register your models here.

