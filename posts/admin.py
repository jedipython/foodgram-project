from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ('title', "slug", "author",) 
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("title",) 
    # добавляем возможность фильтрации по дате
    list_filter = ("author",) 
    empty_value_display = '-пусто-' # это свойство сработает для всех колонок: где пусто - там будет эта строка

# при регистрации модели Post источником конфигурации для неё назначаем класс PostAdmin
admin.site.register(Post, PostAdmin)