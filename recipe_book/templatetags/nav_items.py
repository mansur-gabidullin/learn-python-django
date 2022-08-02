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
        NavItem(reverse('index'), 'Главная'),
        NavItem(reverse('recipes'), 'Рецепты'),
        NavItem(reverse('about_as'), 'О нас'),
    )
