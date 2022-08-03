from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from recipe_book.forms import AddRecipeForm
from recipe_book.models import Recipe, Ingredient, RecipeIngredient, Instruction, Stage, Step


def index(request):
    context = {
        'title': 'Главная',
    }

    return render(request, 'recipe_book/index.html', context=context)


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id)

    context = {
        'title': recipe.title,
        'recipe': recipe
    }

    return render(request, 'recipe_book/recipe.html', context=context)


def recipes(request):
    context = {
        'title': 'Рецепты',
        'recipes': Recipe.objects.all()
    }

    return render(request, 'recipe_book/recipes.html', context=context)


def about_as(request):
    context = {
        'title': 'О нас',
    }

    return render(request, 'recipe_book/about_as.html', context=context)


def add_recipe(request):
    is_post = request.method == 'POST'

    form = AddRecipeForm(request.POST) if is_post else AddRecipeForm()

    context = {
        'title': 'Добавить рецепт',
        'form': form
    }

    if is_post and form.is_valid():
        data = form.cleaned_data
        title = data['title']
        description = data['description']
        ingredients = data['ingredients']
        steps = data['steps']

        with transaction.atomic():
            recipe = Recipe.objects.create(title=title, description=description)
            recipe.save()

            for ingredient_name in ingredients:
                try:
                    ingredient = Ingredient.objects.get(name=ingredient_name)
                except Ingredient.DoesNotExist:
                    ingredient = Ingredient.objects.create(name=ingredient_name)
                    ingredient.save()

                recipe_ingredient = RecipeIngredient(recipe=recipe, ingredient=ingredient)
                recipe_ingredient.save()

            instruction = Instruction.objects.create(recipe=recipe)
            instruction.save()

            stage = Stage.objects.create(instruction=instruction, number=1)
            stage.save()

            for number, step_description in enumerate(steps):
                step = Step.objects.create(stage=stage, number=number, description=step_description)
                step.save()

        return HttpResponseRedirect(reverse('recipes'))

    return render(request, 'recipe_book/add_recipe.html', context=context)
