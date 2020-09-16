from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField('Название ингредиента', max_length=255)
    dimension = models.CharField('Мера измерения', max_length=255)


class Tag(models.Model):

    value = models.CharField('Значение', max_length=50)
    style = models.CharField('Префикс стиля шаблона',
                             max_length=255, null=True)
    name = models.CharField('Имя', max_length=255, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_author")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='recipes')
    text = models.TextField()
    ingredients = models.ManyToManyField(Ingredient,
                                         through='Amount',
                                         through_fields=('recipe', 'ingredient'))
    tags = models.ManyToManyField(Tag)
    time = models.IntegerField()

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
        Post, on_delete=models.CASCADE, related_name="recipe")
