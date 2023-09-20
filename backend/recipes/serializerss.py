from django.db.models import F
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError
from users.models import User
import webcolors

from .models import Ingredients, Recipe, IngredientAmount, Tags
from .validaters import ingredients_exist_validator, tags_exist_validator


class Hex2NameColor(serializers.Field):

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class TagsSerializers(serializers.ModelSerializer):
    color = Hex2NameColor()
    name = serializers.CharField(max_length=200, min_length=1)
    slug = serializers.SlugField(max_length=200)
    id = serializers.IntegerField()

    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug',)


class IngredientsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200, min_length=1)
    measurement_unit = serializers.CharField(min_length=1)
    id = serializers.IntegerField()

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit',)
        read_only_fields = ('__all__',)


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        import base64
        import uuid

        import six
        from django.core.files.base import ContentFile

        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension


class UserSerializers(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('view').request.user

        if user.is_anonymous or (user == obj):
            return False
        return user.follower.filter(author=obj).exists()

    def create_user(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = 'id', 'name', 'image', 'cooking_time'
        read_only_fields = '__all__',


class FollowSerializer(UserSerializers):
    recipes = ShortRecipeSerializer(many=True, read_only=False)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(*args):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()


def recipe_amount_ingredients_set(recipe, ingredients):
    for ingredient in ingredients:
        IngredientAmount.objects.get_or_create(
            recipe=recipe,
            ingredients=ingredient['ingredient'],
            amount=ingredient['amount']
        )


class RecipeSerializers(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200,
                                 validators=[
                                     UniqueValidator(
                                         queryset=Recipe.objects.all()
                                     )
                                 ]
                                 )
    author = UserSerializers(read_only=True)
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = TagsSerializers(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    read_only_fields = (
        'is_favorited',
        'is_in_shopping_cart',
    )

    def validate(self, data):
        tags_ids = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')

        if not tags_ids or not ingredients:
            raise ValidationError('Недостаточно данных.')

        tags_exist_validator(tags_ids, Tags)
        ingredients = ingredients_exist_validator(ingredients, Ingredients)

        data.update({
            'tags': tags_ids,
            'ingredients': ingredients,
            'author': self.context.get('request').user
        })
        return data

    def get_ingredients(self, recipe):
        ingredients = recipe.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('recipe__amount')
        )
        return ingredients

    def get_is_favorited(self, recipe):
        user = self.context.get('view').request.user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('view').request.user
        if user.is_anonymous:
            return False
        return user.shopping_carts.filter(recipe=recipe).exists()

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe_amount_ingredients_set(recipe, ingredients)
        return recipe

    def update(self, recipe, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        for key, value in validated_data.items():
            if hasattr(recipe, key):
                setattr(recipe, key, value)

        if tags:
            recipe.tags.clear()
            recipe.tags.set(tags)

        if ingredients:
            recipe.ingredients.clear()
            recipe_amount_ingredients_set(recipe, ingredients)

        recipe.save()
        return recipe
