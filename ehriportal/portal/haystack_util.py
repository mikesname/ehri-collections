"""Helper classes for dealing with Haystack faceting."""

# TODO: Clean up and refactor

import re
import datetime
from urllib import quote_plus


class FacetClass(object):
    """Class representing a facet with multiple values
    to filter on. i.e. keywords => [foo, bar ...]"""

    FACET_SORT_COUNT = 0
    FACET_SORT_NAME = 1

    def __init__(self, name, prettyname, sort=FACET_SORT_COUNT,
                paramname=None):
        self.name = name
        self.prettyname = prettyname
        self.paramname = paramname if paramname else name
        self.sort = sort
        self.facets = []

    def all_sorted_by_name(self):
        return sorted(self.facets, key=lambda k: k.name)

    def sorted_facets(self):
        if self.sort == self.FACET_SORT_COUNT:
            return self.sorted_by_count()
        return self.sorted_by_name()

    def sorted_by_name(self):
        return [f for f in sorted(self.facets, key=lambda k: k.name) \
                if f.count > 0]

    def sorted_by_count(self):
        return [f for f in sorted(self.facets, key=lambda k: -k.count) \
                if f.count > 0]

    def apply(self, queryset):
        """Apply the facet to the search query set."""
        return queryset.facet(self.name)

    def parse(self, counts, current):
        """Parse the facet_counts structure returns from
        the Haystack query."""
        self.facets = []
        flist = counts.get("fields", {}).get(self.name, [])
        for item, count in flist:
            self.facets.append(Facet(
                item, klass=self, count=count, selected=current))

    def __repr__(self):
        return u"<%s: %s (%d)" % (
                self.__class__.__name__, self.name, len(self.facets))

    def __unicode__(self):
        return self.prettyname

    def narrow(self, queryset, active):
        """Narrow the queryset appropriately if one if
        our points is in the params."""
        for facet in active:
            queryset = queryset.narrow('%s:"%s"' % (self.name,
                queryset.query.clean(facet)))
        return queryset


class QueryFacetClass(FacetClass):
    """Class representing a query facet."""
    def __init__(self, *args, **kwargs):
        facets = kwargs.pop("queries", [])
        super(QueryFacetClass, self).__init__(*args, **kwargs)
        self.facets = facets
        for facet in self.facets:
            facet.klass = self

    def sorted_by_name(self):
        """Name sort should respect the order in which
        the Query facet points were added in the point spec."""
        return [f for f in self.facets if f.count > 0]

    def parse(self, counts, current):
        if not counts.get("queries"):
            return
        for facet in self.facets:
            count = counts["queries"].get("%s_exact:%s" % (
                    self.name, facet.querystr()))
            facet.count = count
            facet._selected = current

    def apply(self, queryset):
        """Apply the facet to the search query set."""
        for facet in self.facets:
            queryset = queryset.query_facet(self.name, facet.querystr())
        return queryset

    def narrow(self, queryset, active):
        """Narrow the queryset appropriately if one if
        our points is in the params."""
        for pname in active:
            # this shouldn't happen unless people diddle with
            # the params, in which case they don't deserve any
            # results
            try:
                point = [p for p in self.facets if str(p) == pname][0]
            except IndexError:
                continue
            queryset = queryset.narrow(point.query())
        return queryset


class Facet(object):
    """Class representing an individual facet constraint,
    i.e. 'language:Afrikaans'."""
    def __init__(self, name, klass=None, count=None,
                selected=[], desc=None):
        self.name = name
        self.klass = klass
        self.count = count
        self.desc = desc
        self._selected = selected

    def prettyname(self):
        return self.desc if self.desc else self.name

    def selected(self):
        return self.filter_name() in self._selected

    def filter_name(self):
        # FIXME: Hack for rare facets with '(', ')', etc
        # in the name, need to find a cleaner way of
        # handling quoting: see 'clean' func in
        # haystack/backends/__init__.py
        def clean(val):
            for char in ['(', ')', '-']:
                val = val.replace(char, '\\%s' % char)
            return val
        return clean('%s:"%s"' % (self.klass.name, self.name))

    def facet_param(self):
        return "%s=%s" % (self.klass.paramname, quote_plus(self.name))


class QueryFacet(Facet):
    """Class representing a Query Facet point."""
    def __init__(self, *args, **kwargs):
        self.point = kwargs.pop("query")
        self.range = isinstance(self.point, tuple)
        super(QueryFacet, self).__init__(str(self), *args, **kwargs)

    def selected(self):
        return self.query() in self._selected

    def query(self):
        return u"%s:%s" % (self.klass.name, self.querystr())

    def querystr(self):
        if self.range:
            return u"[%s TO %s]" % (
                    self._qpoint(self.point[0]),
                        self._qpoint(self.point[1]))
        return str(self.point)

    def filter_name(self):
        return "%s:%s" % (self.klass.name, str(self))

    def _strpoint(self, p):
        if isinstance(p, basestring):
            return ""
        return p

    def _qpoint(self, p):
        if isinstance(p, basestring):
            return "*"
        return p

    def __str__(self):
        if self.range:
            return u"%s_%s" % (
                    self._strpoint(self.point[0]),
                        self._strpoint(self.point[1]))
        return str(self.point)


class DateQueryFacet(QueryFacet):
    """Specialisation of QueryFacet for dates, where
    each point is either a datetime.datetime object
    or a string, such as glob ("*")."""
    def _qpoint(self, p):
        if isinstance(p, basestring):
            return p
        return p.isoformat() + "Z"
