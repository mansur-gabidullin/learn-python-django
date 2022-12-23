from rest_framework import viewsets

from recipe_book.models import Recipe
from recipe_book.serializers import RecipeSerializer

app_name = 'recipe_book'


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
