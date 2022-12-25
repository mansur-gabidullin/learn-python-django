from rest_framework.serializers import ModelSerializer

from recipe_book.models import Recipe, Ingredient, RecipeIngredient, Step


class IngredientOnlySerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(ModelSerializer):
    ingredient = IngredientOnlySerializer(read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    recipe_ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Ingredient
        fields = '__all__'


class StepSerializer(ModelSerializer):
    class Meta:
        model = Step
        fields = '__all__'


class RecipeSerializer(ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True)
    steps = StepSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'
