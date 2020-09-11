from django.urls import path
from . import views

urlpatterns = [
    path("auth/signup/", views.SignUp.as_view(), name="signup"),
    path("subscribes/", views.subscribes, name="subscribes"),
    path("auth/password_change/", views.change_password, name='change_password'),
]
