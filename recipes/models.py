import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from pytils.translit import slugify

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField('Название ингредиента', max_length=255)
    dimension = models.CharField('Мера измерения', max_length=255)

    def __str__(self):
        return self.title


class Tag(models.Model):

    value = models.CharField('Значение', max_length=50)
    style = models.CharField('Префикс стиля шаблона',
                             max_length=255, null=True)
    name = models.CharField('Имя', max_length=255, null=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    def replace_file_name(instance, filename):
        name, ext = filename.split('.')
        filename = f'{instance.slug}.{ext}'
        fullname = os.path.join(settings.MEDIA_ROOT, 'images', filename)
        if os.path.exists(fullname):
            os.remove(fullname)

        return f'images/{filename}'

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recipes")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=replace_file_name)  # поле для картинки
    text = models.TextField()
    ingredients = models.ManyToManyField(Ingredient,
                                         through='Amount',
                                         through_fields=('recipe', 'ingredient'))
    tags = models.ManyToManyField(Tag)
    time = models.IntegerField()
    slug = models.SlugField(editable=False, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'id: {self.pk}, {self.title}'

    @property
    def text_as_list(self):
        return self.text.split('\n')


class Amount(models.Model):
    units = models.IntegerField()
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="ingredients")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="recipe")

    def __str__(self):
        return f'{self.ingredient.title} - {self.units} {self.ingredient.dimension}'

    def create_shopping_list(self):
        return self.ingredient.title, self.units, self.ingredient.dimension


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author')

    def get_recipes(self):
        return Recipe.objects.select_related('author').filter(author=self.author)


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="fav_lists")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='fav_lists')

    def __str__(self):
        return f'{self.recipe}'


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shop_list")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='buy_recipe')
