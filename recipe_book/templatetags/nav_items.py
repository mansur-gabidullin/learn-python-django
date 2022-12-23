from typing import NamedTuple

from django import template
from django.urls import reverse


class NavItem(NamedTuple):
    link: str
    title: str


register = template.Library()


@register.simple_tag
def get_nav_items():
    return (
        NavItem(reverse('recipe_book:index'), 'Главная'),
        NavItem(reverse('recipe_book:recipes'), 'Рецепты'),
        NavItem(reverse('recipe_book:about_us'), 'О нас'),
    )
