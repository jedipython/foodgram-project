import json

from .models import Favorite, ShoppingList, Recipe, Tag
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView


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
            request.session['shopping_list'] = shopping_list
    else:
        request.session['shopping_list'] = [recipe_id]

    return {'success': True}


class RecipeIndexListView(ListView):
    model = Recipe
    template_name = 'index.html'

    def get_queryset(self):
        qs = super().get_queryset()

        if 'filters' in self.request.GET:
            filters = self.request.GET.getlist('filters')
            qs = qs.filter(tags__name__in=filters).distinct()

        return qs

    def get_all_tags(self):
        return Tag.objects.all()

    def context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'all_tags': self.get_all_tags()})
        return context


class RecipeIFavriteListView(ListView):
    model = Favorite
    template_name = 'favorite.html'

    def get_queryset(self):
        qs = super().get_queryset()

        if 'filters' in self.request.GET:
            filters = self.request.GET.getlist('filters')
            qs = qs.filter(recipe__tags__name__in=filters).distinct()

        return qs

    def get_all_tags(self):
        return Tag.objects.all()

    def context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'all_tags': self.get_all_tags()})
        return context