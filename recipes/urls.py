from django.urls import path

from .views import (Ingredients, ProfileUser, RecipeDelete, RecipeEdit,
                    Subscriptions, add_recipe, index, post_view)

app_name = 'recipes'

urlpatterns = [

    path('', index, name="index"),
    path('subscriptions', Subscriptions.as_view(),
         name='add_subscriptions_url'),
    path('api/v1/ingredients', Ingredients.as_view(), name='API'),
    path("add_recipe/", add_recipe, name="add_recipe"),
    path("<slug:slug>", post_view, name="post_url"),
    path('<str:slug>/edit/', RecipeEdit.as_view(),
         name='edit_recipes_url'),
    path('<str:slug>/delete/', RecipeDelete.as_view(),
         name='delete_recipes_url'),
    path('author/<str:username>/', ProfileUser.as_view(),
         name='author_url'),
    path('subscriptions/<int:id>/', Subscriptions.as_view(),
         name='del_subscriptions_url'),

]
