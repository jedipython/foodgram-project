from django import forms
from .models import Recipe
from django.forms.widgets import CheckboxSelectMultiple


class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'text', 'time', 'tags', 'image')
        widgets = {
            "tags": CheckboxSelectMultiple(),
        }
