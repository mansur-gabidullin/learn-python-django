from django.db.models import Model, SlugField, TextField, ManyToManyField, ForeignKey, CASCADE, RESTRICT, OneToOneField, \
    PositiveSmallIntegerField, CharField, DateTimeField


class Ingredient(Model):
    name = SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name


class Recipe(Model):
    title = SlugField(max_length=100, unique=True, allow_unicode=True)
    description = TextField()
    ingredients = ManyToManyField(Ingredient, through='RecipeIngredient')
    created_dt = DateTimeField(auto_now_add=True)
    updated_dt = DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class RecipeIngredient(Model):
    ingredient = ForeignKey(Ingredient, on_delete=RESTRICT)
    recipe = ForeignKey(Recipe, on_delete=RESTRICT)
    amount = CharField(max_length=30)

    def __str__(self):
        return f'{self.ingredient.name} - {self.amount}'


class Instruction(Model):
    recipe = OneToOneField(Recipe, on_delete=CASCADE)

    def __str__(self):
        return f'An instruction for {self.recipe}'


class Stage(Model):
    number = PositiveSmallIntegerField()
    title = SlugField(max_length=100, allow_unicode=True, blank=True)
    instruction = ForeignKey(Instruction, on_delete=RESTRICT, related_name='stages')

    def __str__(self):
        return f'Stage {self.number} for {self.instruction} {f": {self.title}" if self.title else ""}'


class Step(Model):
    number = PositiveSmallIntegerField()
    stage = ForeignKey(Stage, on_delete=RESTRICT, related_name='steps')
    description = TextField()
    ingredients = ManyToManyField(RecipeIngredient, blank=True)

    def __str__(self):
        return f'Step {self.number} for {self.stage}'
