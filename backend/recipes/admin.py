from django.contrib import admin

from .models import (
    Tag, Ingredient, Recipe, Favorite,
    IngredientAmount, Cart
)



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


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Favorite)
admin.site.register(IngredientAmount)
admin.site.register(Cart)
