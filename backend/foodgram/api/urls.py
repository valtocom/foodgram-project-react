from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    IngredientViewSet, RecipeViewSet, TagViewSet,
    SubscribeView, SubscriptionsViewSet
)


router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path(
        'users/subscriptions/',
         SubscriptionsViewSet.as_view({'get': 'list'})
    ),
    path('users/<int:user_id>/subscribe/', SubscribeView.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
