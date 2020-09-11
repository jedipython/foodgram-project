from django.contrib.auth import get_user_model
from django import forms


class AddRecipeForm(forms.ModelForm):
    name = forms.CharField()
    tags = forms.CharField()
    