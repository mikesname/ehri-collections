from urllib import quote
from django.template import Library

register = Library()

@register.filter
def facetparam(name, value):
    """Creates a haystack facet parameter in format:
        sf=<name>_exact:<value>"""
    return "sf=%s%%3A%s" % (quote(name), quote(value))
    
