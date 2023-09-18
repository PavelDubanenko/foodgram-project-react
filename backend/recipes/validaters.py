from recipes.models import Ingredients
from rest_framework.validators import ValidationError


def tags_exist_validator(tags_ids, Tags):
    exists_tags = Tags.objects.filter(id__in=tags_ids)

    if len(exists_tags) != len(tags_ids):
        raise ValidationError('Указан несуществующий тэг')


def ingredients_exist_validator(ingredients, Ingridients):
    ings_ids = [None] * len(ingredients)
    for idx, ing in enumerate(ingredients):
        ingredients[idx]['amount'] = int(ingredients[idx]['amount'])
        if ingredients[idx]['amount'] < 1:
            raise ValidationError('Неправильное количество ингредиента')
        ings_ids[idx] = ing.pop('id', 0)

    ings_in_db_ids = [
        ingredient.id for
        ingredient in
        list(Ingredients.objects.all())]
    ings_in_db_ids.sort()

    for id in range(len(ings_ids)):
        if ings_ids[id] not in ings_in_db_ids:
            raise ValidationError('Ингредиент не существует')

        ingredient = Ingredients.objects.get(pk=ings_ids[id])
        ingredients[id]['ingredient'] = ingredient
    return ingredients