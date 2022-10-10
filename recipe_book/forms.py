from django.core.exceptions import ValidationError
from django.forms import Form, CharField

from recipe_book.models import Recipe


class RecipeForm(Form):
    title = CharField(max_length=100)
    description = CharField()
    ingredients = CharField()
    steps = CharField()

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        mode = self.data.get('mode', 'add')

        if mode == 'add' and Recipe.objects.filter(title=title).exists():
            raise ValidationError("Рецепт с таким названием уже существует.")

        return title

    def clean_ingredients(self):
        ingredients = self.cleaned_data['ingredients']
        return (name.strip() for name in filter(bool, ingredients.splitlines()))

    def clean_steps(self):
        steps = self.cleaned_data['steps']
        return (step.strip() for step in filter(bool, steps.splitlines()))
