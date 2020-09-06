from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    units = models.CharField(max_length=30)


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Post(models.Model):
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="post_author")
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    text = models.TextField()
    ingredients = models.ManyToManyField(Ingredient)
    tag = models.ManyToManyField(Tag)
    time = models.IntegerField()
