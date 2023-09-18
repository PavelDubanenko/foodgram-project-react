import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredients

FILE_PATH = './data/ingredients.csv'
FILE_NAME = FILE_PATH.split('/')[2]


class Command(BaseCommand):
    help = f'Импорт данных {FILE_PATH}'

    def handle(self, *args, **kwargs):

        print(f'Импорт из {FILE_PATH}:')

        with open(f'{FILE_PATH}', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                if Ingredients.objects.filter(
                        name=row['name']).exists() is False:
                    ingredient = Ingredients(
                        name=row['name'],
                        measurement_unit=row['measurement_unit']
                    )
                    ingredient.save()
        print(f'Импоорт {FILE_NAME} завершен.')