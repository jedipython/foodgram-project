from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    url(r'^password_change/$', views.change_password, name='change_password'),
    url(r'^password_reset/$', views.forgot_password, name='password_reset'),
]
