from django.contrib.auth import get_user_model
from django import forms
from .models import Post


class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'time')

    