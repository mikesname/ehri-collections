from urllib import quote
from django.template import Library

register = Library()

from ehriportal.portal import utils

@register.filter
def langname(code):
    """Creates a haystack facet parameter in format:
        &selected_facets=<name>_exact:<value>"""
    return utils.language_name_from_code(code)

