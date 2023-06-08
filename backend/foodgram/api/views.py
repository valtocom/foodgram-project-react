from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAdminAuthorOrReadOnly
from api.serializers import (
    FavoriteSerializer, IngredientSerializer,
    RecipeCreateSerializer, RecipeGetSerializer, ShoppingCartSerializer,
    TagSerialiser, UserSubscribeRepresentSerializer, SubscribeSerializer
)
from api.utils import create_model_instance, create_list
from recipes.models import (
    Favorite, Ingredient, Recipe, RecipeIngredient, Tag
)
from users.models import Subscription, User


class SubscribeView(APIView):
    """Создание и удаление подписок."""
    def post(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        serializer = SubscribeSerializer(
            data={'user': request.user.id, 'author': author.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        if not Subscription.objects.filter(
            user=request.user,
            author=author
        ).exists():
            return Response(
                {'errors': 'Вы не подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Subscription.objects.get(
            user=request.user.id,
            author=user_id
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    """Получение списка всех подписок на пользователей."""
    serializer_class = UserSubscribeRepresentSerializer

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение информации о тегах."""
    queryset = Tag.objects.all()
    serializer_class = TagSerialiser
    permission_classes = (AllowAny, )
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение информации об ингредиентах."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Работа с рецептами. Отправка файла со списком рецептов."""
    queryset = Recipe.objects.all()
    permission_classes = (IsAdminAuthorOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeGetSerializer
        return RecipeCreateSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ]
    )
    def favorite(self, request, pk):
        """Работа с избранными рецептами."""
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            create_model_instance(request, recipe, FavoriteSerializer)
            return Response(
                FavoriteSerializer.data,
                status=status.HTTP_201_CREATED
            )

        if request.method == 'DELETE':
            error_message = 'У вас нет этого рецепта в избранном'

            if not Favorite.objects.filter(
                user=request.user,
                recipe=recipe
            ).exists():
                return Response(
                    {'errors': error_message},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Favorite.objects.filter(user=request.user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ]
    )
    def shopping_cart(self, request, pk):
        """Работа со списком покупок."""
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            create_model_instance(request, recipe, ShoppingCartSerializer)
            return Response(
                ShoppingCartSerializer.data,
                status=status.HTTP_201_CREATED
            )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated, ]
    )
    def download_shopping_cart(self, request):
        """Отправка файла со списком покупок."""
        ingredients = RecipeIngredient.objects.filter(
            recipe__carts__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_amount=Sum('amount'))
        ingredient_name = 'ingredient__name'
        ingredient_unit = 'ingredient__measurement_unit'
        ingredient_amount = 'ingredient_amount'
        create_list(
            ingredients, ingredient_name,
            ingredient_unit, ingredient_amount
        )
