import re
from django.template import Library
from django.conf import settings

register = Library()

@register.filter
def formatattr(value):
    """Formats an object's nested attribute for display"""
    value = value.split(".")[-1]
    return " ".join([p.capitalize() for p in value.split("_")])

