from datetime import datetime as dt
from enum import Enum

from api.pagination import ApiCustomPagination
from django.db.models import F, Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from foodgram.settings import DATE_TIME_FORMAT
from recipes.models import Favorite, Ingredients, Recipe, ShoppingCarts, Tags
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from users.permissions import AuthorOrReadOnly, IsAdminOrReadOnly

from .serializerss import (IngredientsSerializer, RecipeSerializers,
                           ShortRecipeSerializer, TagsSerializers)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializers
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name', '^name__icontains', '^name__trasliterate')

    def get_ingredients(self):
        queryset = self.queryset
        name = self.request.query_params.get('name')
        name = name.lower()
        start_queryset = list(queryset.filter(name__istartswith=name))
        ingridients_set = set(start_queryset)
        cont_queryset = queryset.filter(name__icontains=name)
        start_queryset.extend(
            [ing for ing in cont_queryset if ing not in ingridients_set]
        )
        queryset = start_queryset

        return queryset


class Tuples(tuple, Enum):
    SYMBOL_TRUE_SEARCH = '1', 'true'
    SYMBOL_FALSE_SEARCH = '0', 'false'


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipeSerializers
    permission_classes = [AuthorOrReadOnly]
    pagination_class = ApiCustomPagination
    add_serializer = ShortRecipeSerializer

    def get_queryset(self):
        queryset = self.queryset
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(
                tags__slug__in=tags).distinct()
        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author=author)
        if self.request.user.is_anonymous:
            return queryset
        is_in_shopping_cart = self.request.query_params.get('shopping_carts')
        if is_in_shopping_cart in Tuples.SYMBOL_TRUE_SEARCH.value:
            queryset = queryset.filter(
                in_shopping_carts__user=self.request.user
            )
        elif is_in_shopping_cart in Tuples.SYMBOL_FALSE_SEARCH.value:
            queryset = queryset.exclude(
                in_shopping_carts__user=self.request.user
            )
        is_favorite = self.request.query_params.get('is_favorited')
        if is_favorite in Tuples.SYMBOL_TRUE_SEARCH.value:
            queryset = queryset.filter(
                in_favorites__user=self.request.user
            )
        elif is_favorite in Tuples.SYMBOL_FALSE_SEARCH.value:
            queryset = queryset.exclude(
                in_favorites__user=self.request.user
            )
        return queryset

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,)
            )
    def favorite(self, request, pk):
        recipe = get_object_or_404(self.queryset, pk=pk)
        if request.method == 'POST':
            if Favorite.objects.filter(
                    user=request.user, recipe=recipe
            ).exists():
                raise ValidationError('Этот рецепт уже добавлен')
            Favorite.objects.create(
                user=self.request.user,
                recipe=recipe)
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        in_favorite = Favorite.objects.filter(
            user=request.user,
            recipe=recipe).exists()
        if in_favorite is False:
            raise ValidationError(
                "Рецепт не добавлен в избранное!"
            )
        Favorite.objects.filter(
            user=request.user,
            recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,)
            )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(self.queryset, pk=pk)
        if request.method == 'POST':
            if ShoppingCarts.objects.filter(
                    user=self.request.user,
                    recipe=recipe).exists():
                raise ValidationError(
                    'Этот рецепт уже добавлен'
                )
            ShoppingCarts.objects.create(
                user=self.request.user,
                recipe=recipe)
            serializer = ShortRecipeSerializer(recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        in_shopping_list = ShoppingCarts.objects.filter(
            user=request.user, recipe=recipe).exists()
        if request.method == 'DELETE':
            if in_shopping_list is False:
                raise ValidationError(
                    "Рецепта нет в списке покупок!"
                )
            else:
                ShoppingCarts.objects.filter(
                    user=request.user,
                    recipe=recipe).delete()
                return Response(
                    status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=('get',), detail=False)
    def download_shopping_cart(self, request):
        user = self.request.user
        if not user.shopping_carts.exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST)
        filename = f'{user.username}_shopping_list.txt'
        shopping_carts = [
            f'Список покупок для:\n\n{user.first_name}\n'
            f'{dt.now().strftime(DATE_TIME_FORMAT)}\n'
        ]

        ingredients = Ingredients.objects.filter(
            recipe__recipe__in_shopping_carts__user=user
        ).values(
            'name',
            measurement=F('measurement_unit')
        ).annotate(amount=Sum('recipe__amount'))

        for ing in ingredients:
            shopping_carts.append(
                f'{ing["name"]}: {ing["amount"]} {ing["measurement"]}'
            )
        shopping_carts.append('\nПосчитано в Foodgram')
        shopping_carts = '\n'.join(shopping_carts)
        response = HttpResponse(
            shopping_carts, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
