from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, FormView

from recipe_book.forms import RecipeForm
from recipe_book.models import Recipe, Ingredient, RecipeIngredient, Instruction, Stage, Step


class IndexView(TemplateView):
    template_name = 'recipe_book/index.html'
    extra_context = {'title': 'Главная'}


class RecipesListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    extra_context = {'title': 'Рецепты'}
    template_name = 'recipe_book/recipes.html'


class AboutAsTemplateView(TemplateView):
    extra_context = {'title': 'О нас'}
    template_name = 'recipe_book/about_us.html'


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipe_book/recipe.html'

    def get_context_data(self, **kwargs):
        context = super(RecipeDetailView, self).get_context_data(**kwargs)
        context.update(title=self.object.title)
        return context


class RecipeFormView(AccessMixin, FormView):
    form_class = RecipeForm
    template_name = 'recipe_book/recipe.html'
    success_url = reverse_lazy('recipes')
    http_method_names = ['get', 'post']
    recipe = None
    mode = None

    def dispatch(self, request, *args, **kwargs):
        self.mode = self.kwargs.get('mode')
        has_access = request.user.is_superuser or self.mode == 'view'

        if not has_access:
            return self.handle_no_permission()

        if self.mode == 'view' and request.method == 'POST':
            raise Exception(f'The HTTP method {self.mode} is not allowed in view mode.')

        try:
            pk = int(self.kwargs.get('pk'))
            self.recipe = Recipe.objects.get(pk=pk)
        except (ValueError, TypeError, ObjectDoesNotExist):
            if self.mode != 'add':
                raise Http404()

        return super(RecipeFormView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.mode == 'delete':
            return self.form_valid(self.get_form())
        return super(RecipeFormView, self).post(request, *args, **kwargs)

    def get_initial(self):
        initial = super(RecipeFormView, self).get_initial()
        if self.recipe:
            initial.update(self.recipe.get_fields_values())
        return initial

    def get_context_data(self, **kwargs):
        match self.mode:
            case 'add':
                title = 'Добавление рецепта'
            case 'edit':
                title = f'Редактирование рецепта {self.recipe.title}'
            case 'view':
                title = f'Просмотр рецепта {self.recipe.title}'
            case 'delete':
                title = f'Удаление рецепта {self.recipe.title}'
            case _:
                raise ValueError(f'The mode {self.mode} is not supported.')

        context = super(RecipeFormView, self).get_context_data(**kwargs)
        context.update(title=title, mode=self.mode)

        if self.recipe:
            context.update(recipe=self.recipe, pk=self.recipe.id)

        return context

    def form_valid(self, form):
        title = None
        description = None
        ingredients = None
        steps = None

        if self.mode != 'delete':
            data = form.cleaned_data
            title = data['title']
            description = data['description']
            ingredients = data['ingredients']
            steps = data['steps']

        with transaction.atomic():
            if self.mode == 'add':
                recipe = Recipe.objects.create(title=title, description=description)
            else:
                recipe = self.recipe

            if self.mode == 'edit':
                recipe.title = title
                recipe.description = description
                recipe.save()

            if self.mode == 'edit' or self.mode == 'delete':
                RecipeIngredient.objects.filter(recipe=recipe).delete()
                recipe.ingredients.all().delete()
                Step.objects.filter(stage__instruction__recipe=recipe).delete()
                Stage.objects.filter(instruction__recipe=recipe).delete()
                recipe.instruction.delete()

            if self.mode == 'delete':
                recipe.delete()
            else:
                instruction = Instruction.objects.create(recipe=recipe)
                stage = Stage.objects.create(instruction=instruction, number=1)

                for number, step_description in enumerate(steps, start=1):
                    Step.objects.create(stage=stage, number=number, description=step_description)

                for ingredient_name in ingredients:
                    try:
                        ingredient = Ingredient.objects.get(name=ingredient_name)
                    except Ingredient.DoesNotExist:
                        ingredient = Ingredient.objects.create(name=ingredient_name)

                    RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient)

                for number, step_description in enumerate(steps, start=1):
                    step = stage.steps.get(number=number)
                    step.step_description = step_description
                    step.save()

        return super(RecipeFormView, self).form_valid(form)
