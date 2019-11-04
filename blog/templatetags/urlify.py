from django import template

from urllib.parse import quote_plus

register = template.Library()


@register.filter
def urlify(content):
    return quote_plus(content)
