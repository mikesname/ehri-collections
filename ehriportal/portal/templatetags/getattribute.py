import re
import types
from django.template import Library
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = Library()

@register.filter
def getattribute(value, argstr):
    """Gets an attribute of an object dynamically from a string name"""
    args = argstr.split(".")
    leads = args[:-1]
    arg = args[-1]
    for lead in leads:
        value = getattr(value, lead)
    if hasattr(value, str(arg)):
        val = getattr(value, arg)
        if isinstance(val, types.MethodType):
            return val()
        return val
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID
