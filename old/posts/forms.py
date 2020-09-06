from django import forms
from django.db import models
from .models import Group, Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'title', 'text', 'image')
        required = {'group': False,}

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {'text'}