# Generated by Django 3.2.3 on 2024-09-28 07:54

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='ингредиент')),
                ('measurement_unit', models.CharField(max_length=64, verbose_name='ед. измерения')),
            ],
            options={
                'verbose_name': 'ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='название рецепта')),
                ('text', models.TextField(verbose_name='описание рецепта')),
                ('image', models.ImageField(upload_to='recipes/images/')),
                ('cooking_time', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(9999)], verbose_name='время приготовления')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='автор рецепта')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='тег')),
                ('slug', models.SlugField(max_length=32, unique=True, verbose_name='слаг')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_recipes', to='api.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='api.recipe')),
            ],
            options={
                'unique_together': {('recipe', 'ingredient')},
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='api.RecipeIngredient', to='api.Ingredient', verbose_name='ингредиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='is_favorited',
            field=models.ManyToManyField(related_name='favorited', to=settings.AUTH_USER_MODEL, verbose_name='избранные рецепты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='is_in_shopping_cart',
            field=models.ManyToManyField(related_name='in_cart_of_users', to=settings.AUTH_USER_MODEL, verbose_name='список покупок'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='api.Tag', verbose_name='теги'),
        ),
    ]
