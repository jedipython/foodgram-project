import json

from .models import Favorite, ShoppingList, Recipe
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


def get_fav_list(request):
    """ Функция возвращает список id избранных рецептов. """
    fav_list = []
    if request.user.is_authenticated:
        fav_list = Favorite.objects.select_related('recipe').filter(
            user=request.user).values_list('recipe__id', flat=True)

    return fav_list


def get_buying_list(request):
    """ Функция возвращает список покупок пользователя. """
    if request.user.is_authenticated:
        buying_list = ShoppingList.objects.select_related('recipe').filter(
            user=request.user).values_list('recipe__id', flat=True)
    else:
        buying_list = request.session.get('shopping_list', [])

    return buying_list



def create_buy(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user
    obj, created = ShoppingList.objects.get_or_create(
        defaults={
            'user': user,
            'recipe': recipe,
        },
        user=user,
        recipe=recipe,
    )

    return {'success': bool(created)}


def create_buy_guest(request, recipe_id):
    if 'shopping_list' in request.session:
        shopping_list = request.session['shopping_list']
        recipe_id = int(recipe_id)
        if not recipe_id in shopping_list:
            shopping_list.append(recipe_id)
            request.session['shopping_list'] =shopping_list
    else:
        request.session['shopping_list'] = [recipe_id]

    return {'success': True}