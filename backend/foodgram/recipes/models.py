from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tag(models.Model):
    """Модель для работы с тегами."""
    name = models.CharField(
        verbose_name='Название',
        max_length=150,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цветовой HEX-код',
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Slug',
        max_length=150,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель для работы с ингредиентами."""
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=150,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=150,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Модель для работы с рецептами."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=150,
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/',
        help_text='Добавьте картинку',
        blank=True,
    )
    text = models.TextField(
        verbose_name='Текстовое описание',
        help_text='Добавьте описание рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='RecipeIngredient',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'Автор: {self.author.username} Рецепт: {self.name}'


class RecipeIngredient(models.Model):
    """Модель для объединения рецептов и ингредиентов."""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='recipe',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='ingredient',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество ингредиентов',
    )

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.ingredient} в {self.recipe}'
    

class Favorite(models.Model):
    """Модель для работы со списком избранного."""
    user = models.ForeignKey(
        User,
        related_name='favorite',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorite_recipe',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_favorite'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user} добавил в избранное {self.recipe}'


class ShoppingCart(models.Model):
    """Модель для работы со списком покупок."""
    user = models.ForeignKey(
        User,
        related_name='shopping_cart',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_shopping_cart',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_cart'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return (
            f'{self.user.username} добавил {self.recipe.name} в список покупок'
        )
