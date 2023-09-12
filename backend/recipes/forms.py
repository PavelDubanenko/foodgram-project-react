from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Recipe, Ingredient


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


class CustomRecipesCreationForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'recipes_name',
            'image',
            'description',
            'ingredients',
            'tag',
            'cooking_time',
            'pub_date'
        )


class IngredientsForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = (
            'name',
            'measurement_unit'
        )
