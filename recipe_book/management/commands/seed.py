from time import time

from django.core.management.base import BaseCommand
from django.db import transaction

from ...parser import parse
from recipe_book.models import Recipe


class Command(BaseCommand):
    help = 'Seeding database with data.'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('-t', '--total', type=int, help='Indicates the number of page to be parsed.', )
        parser.add_argument('-s', '--sleep', type=float, help='Sleep in seconds before parse page.', )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        total = kwargs['total']
        sleep_sec = kwargs['sleep']

        self.stdout.write(self.style.HTTP_INFO('Start parsing...'))

        for data in parse(total, sleep_sec=sleep_sec):
            title = data['title']
            self.stdout.write(self.style.HTTP_INFO(f'Parsing recipe: {title}'))

            same_recipe_count = Recipe.objects.filter(title=title).count()

            if same_recipe_count > 0:
                self.stdout.write(self.style.WARNING(f'Found duplicate: {title}'))
                data['title'] = f'[DUPLICATE {time()}] {title}'

            Recipe.add(**data)

        self.stdout.write(self.style.SUCCESS('Done.'))
