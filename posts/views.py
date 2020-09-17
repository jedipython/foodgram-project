from django.shortcuts import render
from .models import Recipe, Tag, Ingredient, Amount, User
from django.core.paginator import Paginator
from .forms import AddRecipeForm
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from .services import get_ingredients
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    post_list = Recipe.objects.order_by("-id").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page,
                                                 "paginator": paginator})


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
    return render(request, 'formRecipe.html', {'form': form, 'tags': tags})


def shop_list(request):
    return render(request, 'shopList.html',)


def favorites(request):
    return render(request, 'favorite.html',)


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
    return render(request, "post.html", {'post': post})


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    post_list = Recipe.objects.filter(author=user).order_by("-id")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "profile.html", {"page": page,
                                            "paginator": paginator})


class RecipeEdit(LoginRequiredMixin, View):
    pass


class RecipeDelete(LoginRequiredMixin, View):
    pass


class Subscriptions(LoginRequiredMixin, View):
    pass
