# Generated by Django 2.2.6 on 2020-09-17 09:37

from django.db import migrations, models

import recipes.models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20200917_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to=recipes.models.Recipe.replace_file_name),
        ),
    ]
