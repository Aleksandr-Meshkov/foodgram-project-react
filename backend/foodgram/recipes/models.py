from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint

from recipes.validators import validate_cooking_time
from users.models import User


class Tag(models.Model):
    """ Модель Теги. """
    name = models.CharField(
        'Название тега', max_length=settings.CHARFIELD_200, unique=True
    )
    color = models.CharField(
        'Цвет', max_length=settings.CHARFIELD_7, unique=True
    )
    slug = models.SlugField(
        'Slug', max_length=settings.CHARFIELD_200, unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """ Модель Ингридиенты. """
    name = models.CharField(
        'Название тега', max_length=settings.CHARFIELD_200
    )
    measurement_unit = models.CharField(
        'Единица измерения', max_length=settings.CHARFIELD_200
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ Модель Рецепты. """
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Теги'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты'
    )
    name = models.CharField(
        'Название рецепта', max_length=settings.CHARFIELD_200
    )
    image = models.ImageField(upload_to='recipes/')
    text = models.TextField('Описание рецепта')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления', validators=[validate_cooking_time]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """ Модель связь Ингридиенты - Рецепты. """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.IntegerField('Колличество')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='recipe_ingredient_unique'
            )
        ]


class TagRecipe(models.Model):
    """ Модель связь Теги - Рецепты. """
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'tag'],
                name='recipe_tag_unique'
            )
        ]


class Favorite(models.Model):
    """ Модель Избранное. """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранное'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='favorite_unique'
            )
        ]


class ShoppingCart(models.Model):
    """ Модель список покупок. """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcart',
        verbose_name='Избранное'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='shoppingcart_unique'
            )
        ]
