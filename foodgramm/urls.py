from django.contrib import admin
from django.urls import path, include
from . import views

handler404 = 'foodgramm.views.page_not_found'
handler500 = 'foodgramm.views.server_error'

urlpatterns = [
    path('404/', views.page_not_found),
    path('500/', views.server_error),
    path('admin/', admin.site.urls),
    path("", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path('', include("posts.urls")),
]
