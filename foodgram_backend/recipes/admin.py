from django.contrib import admin
from .models import (
    User, Tag, Ingredient, Recipe, Follow, Favorite,
    IngredientAmount, Cart
)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'email',
    )
    search_fields = ('username',)
    list_filter = ('email', 'first_name')
    empty_value_display = '-пусто-'


class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'count_favorites'
    )
    filter_horizontal = ['ingredients', 'tags']
    list_filter = ('author', 'name', 'tags')
    empty_value_display = '-пусто-'

    def count_favorites(self, obj):
        return obj.favorites.count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = ('name',)


admin.site.register(User, UserAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Follow)
admin.site.register(Favorite)
admin.site.register(IngredientAmount)
admin.site.register(Cart)
