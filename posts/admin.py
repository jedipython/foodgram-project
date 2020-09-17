from django.contrib import admin
from .models import Post, Amount, Tag


class AmountInline(admin.TabularInline):
    model = Amount
    extra = 1


class PostAdmin(admin.ModelAdmin):

    list_display = ('pk', 'title', "slug", "author",)
    search_fields = ("title",)
    list_filter = ("author",)
    inlines = (AmountInline,)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
