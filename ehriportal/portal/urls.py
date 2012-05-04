from django.conf.urls.defaults import *
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from portal import views, forms, utils

from portal.haystack_util import QueryFacet, FacetClass, QueryFacetClass

def render_entity(entity):
    if entity == "portal.collection":
        return _("Collection")
    elif entity == "portal.repository":
        return _("Repository")
    elif entity == "portal.authority":
        return _("Authority")
    return entity

FACETS = [
    QueryFacetClass(
        "years",
        "Date",
        paramname="date",
        sort=FacetClass.FACET_SORT_NAME,
        queries=[
            QueryFacet(query=("*", 1933), desc="Before 1933"),
            QueryFacet(query=(1933, 1939), desc="1933-1939"),
            QueryFacet(query=1940),
            QueryFacet(query=1941),
            QueryFacet(query=1942),
            QueryFacet(query=1943),
            QueryFacet(query=1944),
            QueryFacet(query=1945),
            QueryFacet(query=(1946, "*"), desc="After 1945"),
        ]
    ),
    FacetClass(
        "languages_of_description",
        "Language of Description",
        paramname="langdesc",
        renderfn=utils.language_name_from_code,
    ),
    FacetClass(
        "django_ct",
        "Type",
        paramname="type",
        renderfn=render_entity,
        raw=True,
    ),
    FacetClass(
        "type_of_entity",
        "Authority Type",
    ),
    FacetClass(
        "languages",
        "Language",
        paramname="lang",
        renderfn=utils.language_name_from_code,
    ),
    FacetClass(
        "location_of_materials",
        "Location of Materials",
        paramname="location",
        renderfn=utils.country_name_from_code,
    ),
    FacetClass(
        "country",
        "Country",
        renderfn=utils.country_name_from_code,
    ),
    FacetClass(
        "tags",
        "Keyword",
        paramname="tag"
    ),
]

urlpatterns = patterns('',
    url(r'^/?$', views.PortalSearchListView.as_view(
        form_class=forms.PortalAllSearchForm,
        facetclasses=FACETS,
        template_name="search.html"), name='search'),
    url(r'^map/?$', views.PortalSearchListView.as_view(
        form_class=forms.MapSearchForm,
        template_name="map.html"), name='map_search'),
    url(r'^/?(?P<facet>[^\/]+)/?$', views.PaginatedFacetView.as_view(
        redirect='search',
        form_class=forms.FacetListSearchForm,
        facetclasses=FACETS),
            name='search_facets'),
)
