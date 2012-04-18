from django.conf.urls.defaults import *

from portal import views, forms

from portal.haystack_util import QueryFacet, FacetClass, QueryFacetClass

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
        paramname="langdesc"
    ),
    FacetClass(
        "type_of_entity",
        "Authority Type",
    ),
    FacetClass(
        "languages",
        "Language",
        paramname="lang"
    ),
    FacetClass(
        "location_of_materials",
        "Location of Materials",
        paramname="location",
    ),
    FacetClass(
        "country",
        "Country",
    ),
    FacetClass(
        "tags",
        "Keyword",
        paramname="tag"
    ),
]

urlpatterns = patterns('',
    url(r'^all/?$', views.PortalSearchListView.as_view(
        form_class=forms.PortalAllSearchForm,
        facetclasses=FACETS,
        template_name="search.html"), name='search'),
    url(r'^all/(?P<facet>[^\/]+)/?$', views.PaginatedFacetView.as_view(
        redirect='search',
        form_class=forms.FacetListSearchForm,
        facetclasses=FACETS),
            name='search_facets'),
    url(r'^search/?$', views.PortalSearchListView.as_view(
        form_class=forms.MapSearchForm,
        template_name="map.html"), name='map_search'),
)
