from django import forms
from .models import *


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'link', 'tags', 'labels', 'upload', 'text', )

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

# class ProfileForm(forms.ModelForm):
#
#     class Meta:
#         model = Author
#         fields = '__all__'


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


# class AuthorEditForm(forms.ModelForm):
#     class Meta:
#         model = Author
#         fields = ('email', 'profile_pic')