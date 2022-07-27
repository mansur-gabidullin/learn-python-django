from django.contrib import admin

from backend.models import Ingredient, Recipe, Instruction, Stage, Step, RecipeIngredient

admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Instruction)
admin.site.register(Stage)
admin.site.register(Step)
