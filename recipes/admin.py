from django.contrib import admin

from .models import Amount, Ingredient, Recipe, Subscription


class AmountInline(admin.TabularInline):
    model = Amount
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', "slug", "author",)
    search_fields = ("title",)
    list_filter = ("author",)
    inlines = (AmountInline,)
    empty_value_display = '-пусто-'


class AmountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'units', "ingredient", "recipe",)
    search_fields = ("ingredient",)
    list_filter = ("ingredient",)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', "title", "dimension",)
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = '-пусто-'


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', "author", "user",)
    search_fields = ("author",)
    list_filter = ("author",)
    empty_value_display = '-пусто-'


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Amount, AmountAdmin)
admin.site.register(Ingredient, IngredientAdmin)
