from django.contrib import admin
from .models import *

admin.site.register(Post)
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'link', 'tags', 'labels', 'text', 'created_date', 'status']
    list_filter = ['status', 'created_date', 'author']
    search_fields = ['title', 'text', 'tags', 'labels']
    raw_id_fields = ['author']
    date_hierarchy = 'created_date'
    ordering = ['status', 'publish']


admin.site.register(Comment)
admin.site.register(Author)