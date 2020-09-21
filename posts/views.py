import json

from django.shortcuts import render
from .models import Recipe, Tag, Ingredient, Amount, User, Subscription, Favorite, ShoppingList
from django.core.paginator import Paginator
from .forms import AddRecipeForm
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from .services import get_ingredients
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .services import get_fav_list, get_buying_list, RecipeIndexListView, ProfileIndexListView, assembly_ingredients, change_ingredients, get_ingredients_value_or_names


class RecipeIndex(RecipeIndexListView, View):
    def get(self, request):
        page = self.get_queryset
        fav_list = get_fav_list(request)
        all_tags = self.get_all_tags
        return render(request, "index.html", {'page': page, 'fav_list': fav_list, 'all_tags': all_tags})


def add_recipe(request):

    if request.method == "POST":
        form = AddRecipeForm(request.POST, files=request.FILES or None)
        ingredients = get_ingredients(request)
        if not bool(ingredients):
            form.add_error(None, 'Добавьте ингредиенты')

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            for item in ingredients:
                Amount.objects.create(
                    units=ingredients[item],
                    ingredient=Ingredient.objects.get(title=f'{item}'),
                    recipe=post)
            form.save_m2m()
            return redirect('/')

    else:
        form = AddRecipeForm(request.POST, files=request.FILES or None)

    tags = Tag.objects.all()
    return render(request, 'formRecipe.html', {'form': form, 'tags': tags, })


class Ingredients(View):
    """ Авто-Заполнение поля ингредиента по API """

    def get(self, request):
        text = request.GET['query']
        ingredients = list(Ingredient.objects.filter(
            title__contains=text).values('title', 'dimension')
        )
        return JsonResponse(ingredients, safe=False)


def post_view(request, slug):
    post = get_object_or_404(Recipe.objects.select_related('author'),
                             slug=slug)
    subsc = False
    fav = False
    if request.user.is_authenticated:
        subsc = Subscription.objects.filter(
            user=request.user, author=post.author).exists()
        fav = Favorite.objects.filter(
            user=request.user, recipe=post).exists()
        buying = ShoppingList.objects.filter(
            user=request.user, recipe=post).exists()
    else:
        buying = request.session.get('shopping_list', [])
        buying = post.id in buying
    return render(request, "post.html", {'post': post, 'subsc': subsc,
                                         'fav': fav,
                                         'buying': buying, })


def single_page(request):
    return render(request, 'customPage.html')



class ProfileUser(ProfileIndexListView, View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        page = self.get_queryset
        all_tags = self.get_all_tags
        # paginator = Paginator(post_list, 10)
        # page_number = request.GET.get('page')
        # page = paginator.get_page(page_number)
        subsc = False
        fav_list = get_fav_list(request)
        buying_list = get_buying_list(request)
        if request.user.is_authenticated:
            subsc = Subscription.objects.filter(
                user=request.user, author=user).exists()
        return render(request, "profile.html", {"page": page, 'user': user, 'subsc': subsc, 'fav_list': fav_list, 'buying_list': buying_list, 'all_tags': all_tags})


class RecipeEdit(LoginRequiredMixin, View):

    def get(self, request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)
        if request.user != recipe.author:
            return redirect('post_url', slug=recipe.slug)

        form = AddRecipeForm(instance=recipe)
        tags = Tag.objects.all()
        return render(request, 'formRecipe.html', context={'form': form, 'recipe': recipe, 'tags': tags})

    def post(self, request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)
        if request.user != recipe.author:
            return redirect('post_url', slug=recipe.slug)

        ingredients = recipe.ingredients.all()
        form = AddRecipeForm(request.POST, request.FILES, instance=recipe)
        ingredients_names = get_ingredients_value_or_names(request, 'name')
        ingredients_values = get_ingredients_value_or_names(request, 'value')
        ingredients_list = assembly_ingredients(ingredients_names, ingredients_values, recipe)
        if form.is_valid():
            form.save()
            change_ingredients(ingredients_list, ingredients, recipe)
        else:
            tags = Tag.objects.all()
            return render(request, 'formRecipe.html', context={'form': form, 'recipe': recipe, 'tags': tags})

        return redirect('post_url', slug=recipe.slug)


class RecipeDelete(LoginRequiredMixin, View):
    def post(self, request, slug):
        recipe = get_object_or_404(Recipe, slug=slug)
        if request.user != recipe.author:
            return redirect('post_url',  slug=recipe.slug)

        recipe.delete()
        return redirect('post_url')


class Subscriptions(LoginRequiredMixin, View):

    def post(self, request):
        author_id = json.loads(request.body)['id']
        author = get_object_or_404(User, id=author_id)

        try:
            Subscription.objects.get_or_create(
                user=request.user, author=author)

            return JsonResponse({'success': True})

        except:
            return JsonResponse({'success': False})

    def delete(self, request, id):
        """ Удаляем подписку если она существует. """
        author = get_object_or_404(User, id=id)
        try:
            subs = Subscription.objects.get(user=request.user, author=author)
        except Subscription.DoesNotExist:
            results = {'success': False}
        else:
            subs.delete()
            results = {'success': True}

        return JsonResponse(results, safe=False, json_dumps_params={'ensure_ascii': False})
