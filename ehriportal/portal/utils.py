"""Utility functions for dealing with repository and geo data."""

import json
import datetime
from types import MethodType  
import babel

from haystack.query import SearchQuerySet
from django.core.paginator import Paginator, Page, InvalidPage, EmptyPage
from django.contrib.gis import geos
from haystack.models import SearchResult
from haystack.query import SearchQuerySet


def language_name_from_code(code, locale="en"):
    """Get lang display name."""
    # TODO: Find the correct way to do this
    return babel.Locale(locale).languages.get(code, "")


def get_country_name_from_code(code, locale="en"):
    """Get the country name from a 2 letter code
    defined in ISO 3166."""
    return babel.Locale(locale).territories.get(code.upper())


def get_script_name_from_code(code, locale="en"):
    """Get the script name from a 4 letter code
    defined in ISO 15924."""
    return babel.Locale(locale).scripts.get(code)


class HaystackPaginationEncoder(json.JSONEncoder):
    """JSON Encoder a Django pagination object."""
    def default(self, obj):
        # handle dates
        if isinstance(obj, geos.Point):
            return (obj.x, obj.y)
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        # handle searchresult objects
        elif isinstance(obj, SearchResult):
            d = dict([(f, getattr(obj, f)) for f in obj.get_stored_fields() \
                    if f != u'suggestions'])
            if obj.location:
                d["location"] = (obj.location.x, obj.location.y)
            return d
        # handle pagination objects
        elif isinstance(obj, Page):
            serializedpage = dict(
                    object_list=[self.default(r) for r in obj.object_list])
            for attr in ("end_index", "has_next", "has_other_pages",
                    "has_previous", "next_page_number", "number",
                    "start_index", "previous_page_number", "object_list"):
                v = getattr(obj, attr)
                if isinstance(v, MethodType):
                    serializedpage[attr] = v()
                elif isinstance(v, (str, int)):
                    serializedpage[attr] = v
                serializedpage["total"] = obj.paginator.count
            return serializedpage        
        return json.JSONEncoder.default(self, obj) 
