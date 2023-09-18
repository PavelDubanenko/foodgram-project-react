from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from colorfield.fields import ColorField

class Ingredients(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=100,
        db_index=True
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=20
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(fields=['name', 'measurement_unit'],
                                    name='unique ingredient')
        ]

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Tags(models.Model):
    name = models.CharField(
        max_length=140,
        blank=False,
        verbose_name='название тега'
    )
    color = ColorField(
        format="hex",
        blank=False,
        verbose_name='Цвет'
    )
    slug = models.SlugField(
        unique=True,
        blank=False,
        verbose_name='индефикатор'
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=150,
        help_text='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/image/',
        verbose_name='Картинка рецепта'
    )
    text = models.TextField(
        verbose_name='Описание',
        max_length=255,
        null=True,
        blank=True,
        help_text='Подробное описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        related_name='recipes',
        through='recipes.IngredientAmount'
    )
    tags = models.ManyToManyField(
        Tags,
        related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name


class IngredientAmount(models.Model):
    ingredients = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='recipe',
        to=Ingredients
    )
    recipe = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='ingredient',
        to=Recipe
    )
    amount = models.PositiveSmallIntegerField(default=0,
                                              verbose_name='Количество',
                                              validators=[MinValueValidator(1)]
                                              )

    class Meta:
        verbose_name = 'Количество',
        verbose_name_plural = 'Количество ингридиентов'
        ordering = ('recipe',)

        constraints = [
            models.UniqueConstraint(
                fields=('ingredients', 'recipe',),
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self) -> str:
        return f'{self.amount} {self.ingredients}'


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique favorite recipe for user')
        ]

    def __str__(self) -> str:
        return f'Пользователь {self.user}\
            добавил рецепт {self.recipe} в избранное'


class ShoppingCarts(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='in_shopping_carts',
        verbose_name='Рецепт добавлен в корзину',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique cart user')
        ]

    def __str__(self):
        return f'Пользователь {self.user} добавил рецепт\
            {self.recipe} в корзину'
