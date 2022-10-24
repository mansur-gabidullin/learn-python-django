from django.test import TestCase
from mixer.backend.django import mixer

from recipe_book.models import Recipe, IngredientNameWithAmount, RecipeIngredient, Step


class TestRecipe(TestCase):
    def setUp(self):
        self.recipe = mixer.blend(Recipe)

    def test_create_ingredients(self):
        name = 'test name'
        amount = 'test amount'
        ingredients = (IngredientNameWithAmount(name, amount),)
        self.recipe.create_ingredients(ingredients)
        recipe_ingredient = self.recipe.ingredients.all()[0]
        self.assertEqual(recipe_ingredient.ingredient.name, name)
        self.assertEqual(recipe_ingredient.amount, amount)

    def test_create_steps(self):
        step1 = 'test step 1'
        step2 = 'test step 2'
        steps = (step1, step2)
        self.recipe.create_steps(steps)
        self.assertEqual(steps[1], self.recipe.steps.all()[1].description)

    def test_remove_recipe_ingredients(self):
        mixer.cycle(5).blend(RecipeIngredient, recipe=self.recipe)
        self.assertEqual(self.recipe.ingredients.count(), 5)
        self.recipe.remove_ingredients()
        self.assertEqual(self.recipe.ingredients.count(), 0)
        self.assertEqual(RecipeIngredient.objects.filter(recipe=self.recipe).count(), 0)

    def test_remove_recipe_steps(self):
        mixer.cycle(5).blend(Step, recipe=self.recipe)
        self.assertEqual(self.recipe.steps.count(), 5)
        self.recipe.remove_steps()
        self.assertEqual(self.recipe.steps.count(), 0)
        self.assertEqual(Step.objects.filter(recipe=self.recipe).count(), 0)

    def test_add_recipe(self):
        self.assertEqual(Recipe.objects.all().count(), 1)

        title = 'test title'
        description = 'test description'
        amount = 'test amount'
        ingredients = (('ingredient1', ''), ('ingredient2', amount))
        steps = ('step1', 'step2')

        data = {
            'title': title,
            'description': description,
            'ingredients': ingredients,
            'steps': steps,
        }

        recipe = Recipe.add(**data)

        self.assertEqual(Recipe.objects.count(), 2)
        self.assertEqual(recipe.title, title)
        self.assertEqual(recipe.description, description)
        self.assertEqual(recipe.description, description)
        self.assertEqual(recipe.ingredients.all()[0].ingredient.name, ingredients[0][0])
        self.assertEqual(recipe.ingredients.all()[0].amount, ingredients[0][1])
        self.assertEqual(recipe.ingredients.all()[1].ingredient.name, ingredients[1][0])
        self.assertEqual(recipe.ingredients.all()[1].amount, ingredients[1][1])
        self.assertEqual(recipe.steps.all()[0].description, steps[0])
        self.assertEqual(recipe.steps.all()[1].description, steps[1])

    def test_edit_recipe(self):
        initial_title = self.recipe.title
        initial_description = self.recipe.description
        title = initial_title + 'edit'
        description = initial_description + 'edit'
        amount = 'test edit amount'
        ingredients = (('edit ingredient1', ''), ('edit ingredient2', amount))
        steps = ('edit step1', 'edit step2')

        data = {
            'title': title,
            'description': description,
            'ingredients': ingredients,
            'steps': steps,
        }

        self.assertNotEqual(self.recipe.title, title)
        self.assertNotEqual(self.recipe.description, description)
        self.assertEqual(self.recipe.ingredients.count(), 0)
        self.assertEqual(self.recipe.steps.count(), 0)

        self.recipe.edit(**data)

        self.assertEqual(self.recipe.title, title)
        self.assertEqual(self.recipe.description, description)
        self.assertEqual(self.recipe.ingredients.count(), 2)
        self.assertEqual(self.recipe.steps.count(), 2)

    def test_recipe_remove(self):
        self.assertEqual(Recipe.objects.count(), 1)
        self.recipe.remove()
        self.assertEqual(Recipe.objects.count(), 0)
