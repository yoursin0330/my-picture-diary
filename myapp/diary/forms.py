from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'mood', 'content', 'painting']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
