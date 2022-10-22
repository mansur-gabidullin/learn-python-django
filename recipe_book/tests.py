from pprint import pprint

from django.forms import model_to_dict
from django.test import TestCase
from mixer.backend.django import mixer

from recipe_book.models import Recipe


class MyTest(TestCase):
    @staticmethod
    def test_mixer():
        recipe = mixer.blend(Recipe)
        pprint(model_to_dict(recipe))
