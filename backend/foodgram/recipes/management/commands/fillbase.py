import csv
import os

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    """Переводит csv файлы в базу данных проекта."""

    help = 'Перевод из csv файлов в модели проекта'

    def fill_ingredient(self):
        """Заполнение модели Ingredient."""
        with open(
            os.path.join('ingredients.csv'),
            'r', encoding='utf-8'
        ) as csv_file:
            data = csv.DictReader(csv_file)
            for row in data:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )

    def handle(self, *args, **options):
        self.fill_ingredient()
