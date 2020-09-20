import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView
from django.core.mail import send_mail
from .forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from posts.models import Subscription, Favorite, Recipe, User, ShoppingList, Amount
from posts.services import get_fav_list, get_id_recipe, create_buy, create_buy_guest
from django.http import HttpResponse, JsonResponse


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = "/auth/login/"
    template_name = "registration/signup.html"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        send_mail_ls(email)
        return super().form_valid(form)


def send_mail_ls(email):
    send_mail('Подтверждение регистрации Продуктовый помощник',
              'Вы зарегистрированы!',
              'ProProduct.ru <admin@proproduct.ru>', [email],
              fail_silently=False)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/changePassword.html', {
        'form': form
    })


def my_subscriptions(request):
    subscriptions = Subscription.objects.filter(user=request.user).all()
    return render(request, 'my_subscription.html', context={'subscriptions': subscriptions})


def my_purchases(request):
    purchases = ShoppingList.objects.filter(user=request.user).all()
    return render(request, 'shopList.html', context={'purchases': purchases})


def my_favorites(request):
    recipes = Favorite.objects.filter(user=request.user).all()
    fav_list = get_fav_list(request)
    return render(request, 'favorite.html', context={'recipes': recipes, 'fav_list': fav_list})


class Favorites(LoginRequiredMixin, View):
    def post(self, request):
        recipe_id = json.loads(request.body)['id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            Favorite.objects.get_or_create(
                user=request.user, recipe=recipe)

            return JsonResponse({'success': True})

        except:
            return JsonResponse({'success': False})

    def delete(self, request, id):
        try:
            fav = Favorite.objects.get(user=request.user, recipe=id)
        except Favorite.DoesNotExist:
            results = {'success': False}
        else:
            fav.delete()
            results = {'success': True}

        return JsonResponse(results, safe=False, json_dumps_params={'ensure_ascii': False})


class Purchases(LoginRequiredMixin, View):
    def post(self, request):
        recipe_id = get_id_recipe(request)
        if request.user.is_authenticated:
            results = create_buy(request, recipe_id)
        else:
            results = create_buy_guest(request, recipe_id)

        return JsonResponse(results, safe=False, json_dumps_params={'ensure_ascii': False})

    def delete(self, request, id):
        try:
            buy = ShoppingList.objects.get(user=request.user, recipe=id)
        except ShoppingList.DoesNotExist:
            results = {'success': False}
        else:
            buy.delete()
            results = {'success': True}
        return JsonResponse(results, safe=False, json_dumps_params={'ensure_ascii': False})


def get_shop_list(request):
    result = create_shopping_list(request)
    filename = 'ShopList.txt'
    response = HttpResponse(result, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        filename)
    return response


def create_shopping_list(request):
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(buy_recipe__user=request.user)
    else:
        buying_list = request.session.get('shopping_list', [])
        recipes = Recipe.objects.filter(id__in=buying_list)
    ingredients = []
    for recipe in recipes:
        ingredient_list = recipe.recipe.all()
        for i in ingredient_list:
            new = i.create_shopping_list()
            ingredients.append(new)
    result = {}
    for i in ingredients:
        if not i[0] in result:
            result[i[0]] = i[1]
        else:
            result[i[0]] += i[1]

    content = []
    for key, value in result.items():
        for i in ingredients:
            if i[0] == key:
                ing = f'{key} - {value} {i[2]}\n'
                content.append(ing)
                break

    return content
