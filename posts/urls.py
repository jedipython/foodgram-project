from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('api/v1/ingredients', views.Ingredients.as_view(), name='API'),
    path("add_recipe/", views.add_recipe, name="add_recipe"),
    path("shop_list/", views.shop_list, name="shop_list"),
    path("favorites/", views.favorites, name="favorites"),
    path("<slug>", views.post_view, name="post_url"),

]