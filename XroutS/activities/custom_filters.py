from django import template

register = template.Library()

@register.filter
def is_multiple_of(value, arg):
    return value % arg == 0