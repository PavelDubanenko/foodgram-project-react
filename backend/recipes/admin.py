from django.contrib import admin
from django.db.models import Count

from .models import (
    Tags, Ingredients, Recipe, Favorite,
    IngredientAmount, ShoppingCarts
)


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    extra = 2


@admin.register(IngredientAmount)
class LinksAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    inlines = (IngredientAmountInline,)
    list_display = (
        'id',
        'name',
        'author',
        'pub_date',
        'get_favorite_count',
    )
    list_filter = ('author', 'tags__name')
    search_fields = ('name', 'author__username')
    autocomplete_fields = ('author',)
    ordering = ('-pub_date',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(favorite_count=Count('in_favorites'))

    @staticmethod
    def get_favorite_count(obj):
        return obj.favorite_count


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('^name', )


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    list_filter = ('name', )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    autocomplete_fields = ('user', 'recipe')


@admin.register(ShoppingCarts)
class ShoppingCartsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    autocomplete_fields = ('user', 'recipe')
