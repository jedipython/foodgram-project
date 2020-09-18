import json

from .models import Recipe, User
from django.shortcuts import get_object_or_404


def get_ingredients(request):

    ingredients = {}
    for key in request.POST:

        if key.startswith('nameIngredient'):
            value_ingredient = key[15:]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + value_ingredient
            ]
    return ingredients


def get_id_recipe(request):
    """ Функция получает id рецепта из тела запроса. """
    body = json.loads(request.body)
    return body.get('id')


# def get_author(request, author=None):
#     """ Функция возвращает автора для создания объекта подписки """
#     if author is None:
#         recipe_id = get_id_recipe(request)
#         author = get_object_or_404(
#             Recipe.objects.select_related('post_author'), id=recipe_id).author
#     else:
#         author = get_object_or_404(User, username=author)
    
#     return author
