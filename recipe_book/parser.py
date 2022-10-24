import time
from typing import Sequence, TypedDict

import requests
from bs4 import BeautifulSoup

from recipe_book.models import IngredientNameWithAmount

_BASE_URL = 'https://www.russianfood.com/recipes'
_RECIPE_URL = f'{_BASE_URL}/recipe.php'
_RECIPE_LIST_URL = f'{_BASE_URL}/bytype/?fid=99'
_ENCODING_HTML = 'windows-1251'
_RECIPE_ID_ATTRIBUTE_NAME = 'data-in_c_id'
_SLEEP_SECONDS = 1.5

_SELECTOR_RECIPE_ID = f'[{_RECIPE_ID_ATTRIBUTE_NAME}]'
_SELECTOR_RECIPE_TITLE = '.center_block .recipe_new .title'
_SELECTOR_RECIPE_DESCRIPTION = '.center_block .recipe_new tr:nth-of-type(2) div > p:only-child'
_SELECTOR_RECIPE_INGREDIENT_WITH_AMOUNT = '.center_block .recipe_new .ingr_block .ingr td:not(.ingr_title) > span'
_SELECTOR_RECIPE_STEP = '.center_block .recipe_new .step_n'


class ParsedRecipeData(TypedDict):
    title: str
    description: str
    ingredients: Sequence[IngredientNameWithAmount]
    steps: Sequence[str]


def _get_soup(page_content):
    return BeautifulSoup(page_content, 'html.parser')


def _get_recipe_list_page_content(*_, session):
    return session.get(_RECIPE_LIST_URL).text


def _get_recipes_ids(*_, session):
    soup = _get_soup(_get_recipe_list_page_content(session=session))
    return (item[_RECIPE_ID_ATTRIBUTE_NAME] for item in soup.select(_SELECTOR_RECIPE_ID))


def _get_recipe_page_content(*_, recipe_id, session, sleep_sec):
    if sleep_sec is None:
        sleep_sec = _SLEEP_SECONDS

    time.sleep(sleep_sec)

    return session.get(_RECIPE_URL, params={'rid': recipe_id}).text


def _parse_recipe_page(*_, recipe_id, session, sleep_sec):
    soup = _get_soup(_get_recipe_page_content(recipe_id=recipe_id, session=session, sleep_sec=sleep_sec))

    data = {
        'title': soup.select_one(_SELECTOR_RECIPE_TITLE).get_text().strip(),
        'description': soup.select_one(_SELECTOR_RECIPE_DESCRIPTION).get_text().strip(),
        'ingredients': (
            IngredientNameWithAmount(*(item.strip() for item in ingredient.get_text().split('-', 1)))
            for ingredient in soup.select(_SELECTOR_RECIPE_INGREDIENT_WITH_AMOUNT)
        ),
        'steps': (step.get_text().strip() for step in soup.select(_SELECTOR_RECIPE_STEP))
    }

    return ParsedRecipeData(**data)


def parse(count=None, sleep_sec=None):
    with requests.Session() as session:
        recipes_ids = _get_recipes_ids(session=session)

        if count:
            recipes_ids = list(recipes_ids)[:count]

        return (
            _parse_recipe_page(recipe_id=recipe_id, session=session, sleep_sec=sleep_sec)
            for recipe_id in recipes_ids
        )


if __name__ == '__main__':
    print(list(parse(count=1)))
