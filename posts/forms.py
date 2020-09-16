from django import forms
from .models import Post
from django.forms.widgets import CheckboxSelectMultiple


class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'time', 'tags', 'image' )
        widgets = {
            "tags": CheckboxSelectMultiple(),
        }
