import base64

from django.shortcuts import HttpResponse, get_object_or_404
from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Ingredient, RecipeIngredient


class Base64ImageField(serializers.ImageField):
    """Класс для работы с изображениями."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


def create_ingredients(ingredients, recipe):
    """Функция для добавления ингредиентов."""
    ingredient_list = []
    for ingredient in ingredients:
        current_ingredient = get_object_or_404(
            Ingredient,
            id=ingredient.get('id')
        )
        amount = ingredient.get('amount')
        ingredient_list.append(
            RecipeIngredient(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=amount
            )
        )
    RecipeIngredient.objects.bulk_create(ingredient_list)


def create_model_instance(request, instance, serializer_name):
    """Функция для добавления рецепта в избранное и в список покупок."""
    serializer = serializer_name(
        data={'user': request.user.id, 'recipe': instance.id, },
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()


def create_list(ingredient_list, name, unit, amount):
    shopping_list = ['Список покупок:\n']
    for ingredient in ingredient_list:
        name = ingredient[name]
        unit = ingredient[unit]
        amount = ingredient[amount]
        shopping_list.append(f'\n{name} - {amount}, {unit}')
    response = HttpResponse(shopping_list, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="shopping_cart.txt"'
    return response    
