from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from recipe_book.api_views import RecipeViewSet, IngredientViewSet, RecipeIngredientViewSet, StepViewSet
from recipe_book.views import IndexView, RecipesListView, AboutAsTemplateView, RecipeFormView

app_name = 'recipe_book'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    re_path(r'^recipe/(?P<mode>add|view|edit|delete)/(?P<pk>\d+)?$', RecipeFormView.as_view(), name='recipe'),
    path('recipes/', RecipesListView.as_view(), name='recipes'),
    path('about_us/', AboutAsTemplateView.as_view(), name='about_us'),
]

router = DefaultRouter()

router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipe-ingredients', RecipeIngredientViewSet)
router.register(r'steps', StepViewSet)
