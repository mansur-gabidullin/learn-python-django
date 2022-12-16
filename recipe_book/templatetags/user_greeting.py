from django import template

register = template.Library()


@register.filter
def greeting(user):
    name = user.get_short_name() or user.first_name or user.email
    return f'Привет {name}'
