from django.urls import path

from recipe_book.views import index, recipe, recipes, about_as, add_recipe

urlpatterns = [
    path('', index, name='index'),
    path('recipe/<int:id>', recipe, name='recipe'),
    path('recipes', recipes, name='recipes'),
    path('about_as', about_as, name='about_as'),
    path('add_recipe', add_recipe, name='add_recipe'),
]
