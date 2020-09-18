from django.shortcuts import render
from .models import Recipe, Tag, Ingredient, Amount, User, Subscription, Favorite, ShoppingList
from django.core.paginator import Paginator
from .forms import AddRecipeForm
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from .services import get_ingredients, get_author
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
    return render(request, 'formRecipe.html', {'form': form, 'tags': tags, })


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
    def get(self, request):
        author = request.GET.get('author')
        if 'sub' in request.GET:
            get_object_or_404(Subscription.objects.select_related('author'),
                              user=request.user, author__username=author).delete()
        else:
            self.post(request, author)

        return redirect('author_url',  username=author)

    def post(self, request, author=None):
        """ Создание подписки на автора если ее еще нет. """
        author = get_author(request, author)
        user = request.user
        subs, created = Subscription.objects.get_or_create(
            defaults={
                'user': user,
                'author': author,
            },
            user=user,
            author=author,
        )
        if created:
            results = {'success': True}
        else:
            results = {'success': False}
        return JsonResponse(results, safe=False, json_dumps_params={'ensure_ascii': False})

    def delete(self, request, id):
        """ Удаляем подписку если она существует. """
        author = get_object_or_404(
            Recipe.objects.select_related('author'), id=id).author
        try:
            subs = Subscription.objects.get(user=request.user, author=author)
        except Subscription.DoesNotExist:
            results = {'success': False}
        else:
            subs.delete()
            results = {'success': True}

        return JsonResponse(results, safe=False, json_dumps_params={'ensure_ascii': False})
