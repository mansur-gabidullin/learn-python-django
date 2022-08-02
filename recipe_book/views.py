from django.shortcuts import render


def index(request):
    context = {
        'title': 'Главная',
    }

    return render(request, 'recipe_book/index.html', context=context)


def recipes(request):
    context = {
        'title': 'Рецепты',
    }

    return render(request, 'recipe_book/recipes.html', context=context)


def about_as(request):
    context = {
        'title': 'О нас',
    }

    return render(request, 'recipe_book/about_as.html', context=context)


def add_recipe(request):
    context = {
        'title': 'Добавить рецепт',
    }

    return render(request, 'recipe_book/add_recipe.html', context=context)
