import re

from django.template import Library

register = Library()

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
def stripparam(url, paramname):
    """Removes a param AND its value from an URL, taking care of
    the ? or & parts."""
    urlstr = re.sub("[&]?" + paramname + "=(?:[^\?&]+)?", "", url).replace("&&", "&")
    if urlstr.endswith(("?", "&")):
        urlstr = urlstr[:-1]
    return urlstr
    
    
