from typing import NamedTuple, Sequence

from django.db import transaction
from django.db.models import (
    Model,
    TextField,
    ManyToManyField,
    ForeignKey,
    RESTRICT,
    PositiveSmallIntegerField,
    CharField,
    DateTimeField
)


class IngredientWithAmount(NamedTuple):
    name: str
    amount: str = ''


class Ingredient(Model):
    name = CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Recipe(Model):
    title = CharField(max_length=100, unique=True)
    description = TextField()
    ingredients = ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name="ingredients",
        related_query_name="ingredient"
    )
    created_dt = DateTimeField(auto_now_add=True)
    updated_dt = DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @transaction.atomic
    def create_ingredients(self, ingredients: Sequence[IngredientWithAmount]):
        for name, amount in ingredients:
            try:
                ingredient = Ingredient.objects.get(name=name)
            except Ingredient.DoesNotExist:
                ingredient = Ingredient.objects.create(name=name)

            RecipeIngredient.objects.create(recipe=self, ingredient=ingredient, amount=amount)

    @transaction.atomic
    def create_steps(self, steps):
        for number, step_description in enumerate(steps, start=1):
            Step.objects.create(recipe=self, number=number, description=step_description)

    @transaction.atomic
    def remove_ingredients(self):
        RecipeIngredient.objects.filter(recipe=self).delete()

    @transaction.atomic
    def remove_steps(self):
        self.steps.delete()

    @staticmethod
    @transaction.atomic
    def add(*_, title, description, ingredients: Sequence[IngredientWithAmount], steps):
        recipe = Recipe.objects.create(title=title, description=description)
        recipe.create_ingredients(ingredients)
        recipe.create_steps(steps)

    @transaction.atomic
    def edit(self, *_, title, description, ingredients: Sequence[IngredientWithAmount], steps):
        self.title = title
        self.description = description
        self.save()
        self.remove_ingredients()
        self.remove_steps()
        self.create_ingredients(ingredients)
        self.create_steps(steps)

    @transaction.atomic
    def remove(self):
        self.remove_ingredients()
        self.remove_steps()
        self.delete()

    def get_fields_values(self):
        return {
            'title': self.title,
            'description': self.description,
            'ingredients': '\n'.join(i.name for i in self.ingredients.all()),
            'steps': '\n'.join(step.description for step in self.steps.all()),
        }


class RecipeIngredient(Model):
    ingredient = ForeignKey(Ingredient, on_delete=RESTRICT)
    recipe = ForeignKey(Recipe, on_delete=RESTRICT)
    amount = CharField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.ingredient.name} {self.amount if f" - {self.amount}" else ""} для {self.recipe}'


class Step(Model):
    class Meta:
        unique_together = (('recipe', 'number'),)

    recipe = ForeignKey(Recipe, on_delete=RESTRICT, related_name='steps')
    number = PositiveSmallIntegerField()
    description = TextField()

    def __str__(self):
        return f'Step {self.number} for {self.recipe}'
