from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView

from recipe_book.forms import RecipeForm
from recipe_book.models import Recipe, IngredientNameWithAmount


class IndexView(TemplateView):
    template_name = 'recipe_book/index.html'
    extra_context = {'title': 'Главная'}
    http_method_names = ['get']


class RecipesListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    extra_context = {'title': 'Рецепты'}
    template_name = 'recipe_book/recipes.html'
    http_method_names = ['get']
    paginate_by = 5


class AboutAsTemplateView(TemplateView):
    extra_context = {'title': 'О нас'}
    template_name = 'recipe_book/about_us.html'
    http_method_names = ['get']


class RecipeFormView(AccessMixin, FormView):
    form_class = RecipeForm
    template_name = 'recipe_book/recipe.html'
    success_url = reverse_lazy('recipes')
    http_method_names = ['get', 'post']
    recipe = None
    mode = None

    def dispatch(self, request, *args, **kwargs):
        self.mode = self.kwargs.get('mode')
        pk_arg = self.kwargs.get('pk')
        has_access = request.user.is_superuser or self.mode == 'view'

        if not has_access or self.mode == 'view' and request.method == 'POST':
            return self.handle_no_permission()

        try:
            pk = int(pk_arg)
        except (ValueError, TypeError):
            pk = None

        if not pk and self.mode != 'add':
            raise Http404

        try:
            self.recipe = Recipe.objects.prefetch_related('ingredients', 'steps').get(pk=pk)
        except ObjectDoesNotExist as error:
            if self.mode != 'add':
                raise error

        return super(RecipeFormView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.mode == 'delete':
            return self.form_valid(self.get_form())
        return super(RecipeFormView, self).post(request, *args, **kwargs)

    def get_initial(self):
        initial = super(RecipeFormView, self).get_initial()
        if self.recipe:
            initial.update({
                'title': self.recipe.title,
                'description': self.recipe.description,
                'ingredients': '\n'.join(i.ingredient.name for i in self.recipe.ingredients.all()),
                'steps': '\n'.join(step.description for step in self.recipe.steps.all()),
            })
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
        data = {}

        if self.mode != 'delete':
            data = form.cleaned_data
            data['ingredients'] = (IngredientNameWithAmount(name, amount='') for name, amount in data['ingredients'])

        match self.mode:
            case 'add':
                Recipe.add(**data)
            case 'edit':
                self.recipe.edit(**data)
            case 'delete':
                self.recipe.remove()
            case _:
                raise ValueError(f'{self.mode} is not supported')

        return super(RecipeFormView, self).form_valid(form)
