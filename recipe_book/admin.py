from django.contrib import admin

from recipe_book.models import Ingredient, Recipe, Step, RecipeIngredient

admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Step)
