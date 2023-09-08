from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Кастомизированная модель юзера"""
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=False,
        help_text='Имя Пользователя'
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=False,
        help_text='Фамилия пользователя'
    )
    username = models.SlugField(
        verbose_name='Никнейм',
        max_length=150,
        unique=True,
        null=False,
        help_text='Введите имя пользователя'
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=254,
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=100,
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


class Tag(models.Model):
    BLUE = '#0000FF'
    ORANGE = '#FFA500'
    GREEN = '#008000'
    PURPLE = '#800080'
    YELLOW = '#FFFF00'

    COLOR_CHOICES = [
        (BLUE, 'Синий'),
        (ORANGE, 'Оранжевый'),
        (GREEN, 'Зеленый'),
        (PURPLE, 'Фиолетовый'),
        (YELLOW, 'Желтый'),
    ]
    name = models.CharField(
        unique=True,
        verbose_name='Тэг',
        max_length=64,
        help_text='Пример: Завтрак, Обед, Ужин')
    color = models.CharField(
        max_length=7,
        unique=True,
        choices=COLOR_CHOICES,
        verbose_name='Цвет в HEX')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
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
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингридиенты',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        help_text='Введите время приготовления от 1 до 9999 минут',
        validators=(
            MinValueValidator(limit_value=1,
                              message='Время приготовления \
                                не может быть меньше 1 минуты'),
            MaxValueValidator(limit_value=9999,
                              message='Время приготовления \
                                не может быть больше 9999 минут')
        )
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Кол-во',
        help_text='Количество ингридиентов от 1 до 9999',
        validators=(
            MinValueValidator(limit_value=1,
                              message='Ингридиентов не может быть меньше 1'),
            MaxValueValidator(limit_value=999,
                              message='Ингридиентов не может быть больше 9999')
        )
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique ingredients recipe')
        ]

    def __str__(self):
        return f'В рецепт {self.recipe} необходимо добавить\
            {self.ingredient} {self.amount}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique follow',
            )
        ]

    def __str__(self):
        return f'Пользователь {self.user} \
            подписался на {self.author}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
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


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
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
