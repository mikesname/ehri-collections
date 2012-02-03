from urllib import quote
from django.template import Library

register = Library()

@register.filter
def facetparam(name, value):
    """Creates a haystack facet parameter in format:
        selected_facets=<name>_exact:<value>"""
    return "selected_facets=%s%%3A%s" % (quote(name), quote(value))
    
