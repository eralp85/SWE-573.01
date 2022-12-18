from django import forms
from .models import *
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'link', 'tags', 'labels', 'upload', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text', )

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = '__all__'

