from django.urls import path
from . import views

urlpatterns = [
    path("auth/signup/", views.SignUp.as_view(), name="signup"),
    path("my_sub/", views.my_subscriptions, name="my_subscriptions"),
    path("my_favorites/", views.my_favorites, name="my_favorites"),
    path("shop_list/", views.my_purchases, name="shop_list"),
    path('favorites/<int:id>/', views.Favorites.as_view(), name='del_favorites_url'),
    path('favorites', views.Favorites.as_view(), name='favorites_url'),
    path('purchases', views.Purchases.as_view(), name='purchases'),
    path('purchases/<int:id>/', views.Purchases.as_view(), name='del_purchase'),
    path("auth/password_change/", views.change_password, name='change_password'),
    path("get_shop_list/", views.get_shop_list, name='get_shop_list_url'),

]
