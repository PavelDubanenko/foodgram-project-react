from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Recipes, Ingredients


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields


class CustomRecipesCreationForm(forms.ModelForm):
    class Meta:
        model = Recipes
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
        model = Ingredients
        fields = (
            'name',
            'measurement_unit'
        )
