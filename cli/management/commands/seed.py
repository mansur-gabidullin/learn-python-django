from django.core.management.base import BaseCommand
from django.db import transaction

from ...parser import parse
from backend.models import Step, Stage, Instruction, Recipe, RecipeIngredient, Ingredient


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

        for title, description, ingredients, steps in parse(total, sleep_sec=sleep_sec):
            self.stdout.write(self.style.HTTP_INFO(f'Parsing recipe: {title}'))

            try:
                same_recipe_count = Recipe.objects.filter(title=title).count()
                title = f'[DUPLICATE {same_recipe_count + 1}] {title}'
                recipe = Recipe.objects.create(title=title, description=description)
                self.stdout.write(self.style.WARNING(f'Found duplicate: {title}'))
            except Ingredient.DoesNotExist:
                recipe = Recipe.objects.create(title=title, description=description)

            recipe.save()

            for name, amount in ingredients:
                self.stdout.write(self.style.HTTP_INFO(f'Parsing ingredient: {name}'))

                try:
                    ingredient = Ingredient.objects.get(name=name)
                except Ingredient.DoesNotExist:
                    ingredient = Ingredient.objects.create(name=name)
                    ingredient.save()

                recipe_ingredient = RecipeIngredient(recipe=recipe, ingredient=ingredient, amount=amount)
                recipe_ingredient.save()

            instruction = Instruction.objects.create(recipe=recipe)
            instruction.save()

            stage = Stage.objects.create(instruction=instruction, number=1)
            stage.save()

            for number, step_description in enumerate(steps):
                self.stdout.write(self.style.HTTP_INFO(f'Parsing step: {number}'))

                step = Step.objects.create(stage=stage, number=number, description=step_description)
                step.save()

        self.stdout.write(self.stdout.write(self.style.SUCCESS('Done.')))
