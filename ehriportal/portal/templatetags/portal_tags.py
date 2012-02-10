import re

from django.template import Library
from django.utils.http import urlquote_plus

from portal import utils

register = Library()

@register.filter
def quote_plus(string):
    return urlquote_plus(string)

@register.filter
def addparam(url, param):
    """Appends or removes a param from an URL"""
    if "?" in url:
        return "%s&%s" % (url, param)
    return "%s?%s" % (url, param)

@register.filter
def removeparam(url, param):
    """Removes a param from an URL, taking care of
    the ? or & parts."""
    urlstr = url.replace(param, "").replace("&&", "&")
    if urlstr.endswith(("?", "&")):
        urlstr = urlstr[:-1]
    return urlstr

@register.filter
def stripparam(url, paramnames):
    """Removes a param AND its value from an URL, taking care of
    the ? or & parts."""
    params = paramnames.split(",")
    for param in params:
        url = re.sub("&" + param + "=(?:[^\?&]+)?", "", url)
        url = re.sub("\?" + param + "=(?:[^\?&]+)?", "?", url)\
                .replace("&&", "&")\
                .replace("?&", "?")
    if url.endswith(("?", "&")):
        url = url[:-1]
    return url
    
@register.filter
def langcode2name(code):
    """Creates a haystack facet parameter in format:
        &selected_facets=<name>_exact:<value>"""
    return utils.language_name_from_code(code)

@register.filter
def us2title(value):
    """Formats an object's nested attribute for display"""
    value = value.split(".")[-1]
    return " ".join([p.capitalize() for p in value.split("_")])

    
