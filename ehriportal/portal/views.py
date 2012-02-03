# Create your views here.

import re
from urllib import quote

from haystack.views import FacetedSearchView
from haystack.query import SearchQuerySet

# Crime against programming
DATEMATH = re.compile("\[(?:(?P<from>\d{4})|(\*))[\s-].*?TO (?:(?P<to>\d{4})|(\*)).*?\]")


class FacetClass(object):
    """Class representing a facet with multiple values
    to filter on. i.e. keywords => [foo, bar ...]"""
    def __init__(self, name, prettyname, results):
        self.name = name
        self.prettyname = prettyname
        self.results = results
        self.facets = []

    def sorted_by_name(self):
        return sorted(self.facets, key=lambda k: k.name)


class Facet(object):
    def __init__(self, klass, name, count, pretty=None, query=False):
        self.name = name
        self.klass = klass
        self.count = count
        self.query = query
        self.prettyname = pretty if pretty else name

    def filter_name(self):
        if self.query:
            return '%s:%s' % (self.klass.name, self.name)
        return '%s:"%s"' % (self.klass.name, self.name)

    def facet_param(self):
        return "selected_facets=%s%%3A%s" % (quote(self.klass.name), quote(self.name))

    def is_selected(self):
        return self.filter_name() in self.klass.results.query.narrow_queries


class PortalSearchView(FacetedSearchView):
    def __init__(self, *args, **kwargs):
        self.apply_facets = kwargs.pop("apply_facets", {})
        super(PortalSearchView, self).__init__(*args, **kwargs)

        if self.searchqueryset is None:
            self.searchqueryset = SearchQuerySet()
        for facet in self.apply_facets.keys():
            self.searchqueryset = self.searchqueryset.facet(facet)

    def extra_context(self, *args, **kwargs):
        extra = super(PortalSearchView, self).extra_context(*args, **kwargs)

        # we need to process out facets in a way that makes it easy to
        # render them without too much horror in the template.
        extra["facet_names"] = self.apply_facets

        facetclasses = []
        # this is oh so gross at the moment. Now I have two problems...
        # This regexp matches query facets with the DATE pattern:
        # field:[<DATE> TO <DATE>]
        qfmatch = re.compile("(?P<fname>[^:]+):(?P<facet>" + DATEMATH.pattern + ")")
        if extra.get("facets") and extra.get("facets").get("queries"):
            qclasses = {}
            for facet, num in extra["facets"]["queries"].iteritems():
                mf = qfmatch.match(facet)
                if not mf:
                    raise ValueError("Query didn't match expected pattern: '%'" % facet)
                classname = mf.group("fname")
                fc = qclasses.get(classname)
                if not fc:
                    fc = FacetClass(classname, classname.capitalize(), self.results)
                    qclasses[classname] = fc
                facet = Facet(fc, mf.group("facet"), num, query=True)
                if mf.group("from") is None:
                    facet.prettyname = "Before %s" % mf.group("to")
                elif mf.group("to") is None:
                    facet.prettyname = "Since %s" % mf.group("from")
                else:
                    facet.prettyname = "%s-%s" % (mf.group("from"), mf.group("to"))
                fc.facets.append(facet)
            facetclasses.extend(qclasses.values())

        for key, pretty in self.apply_facets.iteritems():
            flist = extra["facets"]["fields"][key]

            facetclass = FacetClass(key, pretty, self.results)
            for item, count in flist:
                facetclass.facets.append(Facet(facetclass, item, count))
            facetclasses.append(facetclass)
                
        extra["facet_classes"] = facetclasses
        return extra


class PaginatedFacetView(PortalSearchView):

    # MASSIVE HACK: SearchView is broken WRT switching
    # templates in response to request params, such as
    # whether or not it's an Ajax request.
    # So overriding __call__ to fix this.
    def __call__(self, request):
        if request.is_ajax():
            self.template = "portal/_expand_facet_list.html"
        self.template = "portal/facets.html"
        return super(PaginatedFacetView, self).__call__(request)


