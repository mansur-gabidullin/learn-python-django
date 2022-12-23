from rest_framework import serializers

from recipe_book.models import Recipe


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
