from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CustomUserViewSet, IngredientsViewSet,
                    RecipeViewSet, TagsViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('users', CustomUserViewSet)
router.register('recipes', RecipeViewSet)
router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
