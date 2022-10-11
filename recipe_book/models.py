from django.db.models import Model, TextField, ManyToManyField, ForeignKey, CASCADE, RESTRICT, OneToOneField, \
    PositiveSmallIntegerField, CharField, DateTimeField


class Ingredient(Model):
    name = CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Recipe(Model):
    title = CharField(max_length=100, unique=True)
    description = TextField()
    ingredients = ManyToManyField(
        Ingredient, through='RecipeIngredient', related_name="ingredients", related_query_name="ingredient"
    )
    created_dt = DateTimeField(auto_now_add=True)
    updated_dt = DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_fields_values(self):
        steps = (step for stage in self.instruction.stages.all() for step in stage.steps.all())
        return {
            'title': self.title,
            'description': self.description,
            'ingredients': '\n'.join(i.name for i in self.ingredients.all()),
            'steps': '\n'.join(step.description for step in steps),
        }


class RecipeIngredient(Model):
    ingredient = ForeignKey(Ingredient, on_delete=RESTRICT)
    recipe = ForeignKey(Recipe, on_delete=RESTRICT)
    amount = CharField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.ingredient.name}{self.amount if f" - {self.amount}" else ""}'


class Instruction(Model):
    recipe = OneToOneField(Recipe, on_delete=CASCADE)

    def __str__(self):
        return f'An instruction for {self.recipe}'


class Stage(Model):
    number = PositiveSmallIntegerField(unique=True)
    title = CharField(max_length=100, blank=True)
    instruction = ForeignKey(Instruction, on_delete=RESTRICT, related_name='stages')

    def __str__(self):
        return f'Stage {self.number} for {self.instruction} {f": {self.title}" if self.title else ""}'


class Step(Model):
    number = PositiveSmallIntegerField(unique=True)
    stage = ForeignKey(Stage, on_delete=RESTRICT, related_name='steps')
    description = TextField()
    ingredients = ManyToManyField(RecipeIngredient, blank=True)

    def __str__(self):
        return f'Step {self.number} for {self.stage}'
