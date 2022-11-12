import csv

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from recipes.models import Ingredient, Tag


class Command(BaseCommand):

    def handle(self, *args, **options):
        file_name = 'recipes/data/ingredients.csv'
        with open(file_name, 'r', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                name, measurement_unit = row
                try:
                    Ingredient.objects.create(
                        name=name,
                        measurement_unit=measurement_unit
                    )
                except IntegrityError:
                    print(f'Ингредиент {name} {measurement_unit}'
                          f'уже есть в базе')
        file_name = 'recipes/data/tags.csv'
        with open(file_name, 'r', encoding='utf-8') as file:
            file_reader = csv.reader(file)
            for row in file_reader:
                name, color, slug = row
                try:
                    Tag.objects.create(
                        name=name,
                        color=color,
                        slug=slug
                    )
                except IntegrityError:
                    print(f'Тег {name} уже есть в базе')
