# Generated by Django 2.2.6 on 2020-09-16 13:36

import json

from django.db import migrations, transaction


def add_ingredients(apps, schema_editor):
    Ingredient = apps.get_model('recipes', 'Ingredient')
    Ingredient.objects.all().delete()
    with open('ingredients.json', encoding='utf-8') as file:
        ingredients = json.load(file)
        for ingredient in ingredients:
            with transaction.atomic():
                Ingredient.objects.create(
                    title=ingredient['title'],
                    dimension=ingredient['dimension'])


def add_tags(apps, schema_editor):
    Tag = apps.get_model('recipes', 'Tag')
    Tag.objects.all().delete()
    with open('tags.json', encoding='utf-8') as file:
        tags = json.load(file)
        for tag in tags:
            with transaction.atomic():
                Tag.objects.create(
                    value=tag['value'], style=tag['style'],
                    name=tag['name'])


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_ingredients),
        migrations.RunPython(add_tags),
    ]
