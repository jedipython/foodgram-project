from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from .models import Recipe


class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'text', 'time', 'tags', 'image')
        widgets = {
            "tags": CheckboxSelectMultiple(),
        }
