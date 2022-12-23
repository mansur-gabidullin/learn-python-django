from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from recipe_book.models import Recipe, Ingredient, RecipeIngredient, Step
from recipe_book.permissions import DeleteOnlyAdminUser
from recipe_book.serializers import RecipeSerializer, IngredientSerializer, RecipeIngredientSerializer, StepSerializer

app_name = 'recipe_book'


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Recipe.objects.prefetch_related('ingredients', 'ingredients__ingredient', 'steps').all()
    serializer_class = RecipeSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    permission_classes = [DeleteOnlyAdminUser]
    queryset = Ingredient.objects.prefetch_related('recipe_ingredients').all()
    serializer_class = IngredientSerializer


class RecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer


class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
