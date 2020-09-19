from django.urls import path
from . import views

urlpatterns = [
    path("auth/signup/", views.SignUp.as_view(), name="signup"),
    path("my_sub/", views.my_subscriptions, name="my_subscriptions"),
    path("favorites/", views.my_favorites, name="my_favorites"),
    path("auth/password_change/", views.change_password, name='change_password'),

]
