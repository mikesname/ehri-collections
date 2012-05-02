from django.conf.urls.defaults import *
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import update_object
from django.contrib.auth.decorators import login_required, user_passes_test

from portal import views, forms, models, permissions
from portal.haystack_util import FacetClass

from haystack.query import SearchQuerySet

FACETS = [
    FacetClass(
        "type_of_entity",
        "Authority Type",
    )
]


urlpatterns = patterns('',
    url(r'^search/?$', views.PortalSearchListView.as_view(
        model=models.Authority,
        facetclasses=FACETS,
        template_name="authority_search.html"), name='authority_search'),
    url(r'^search/(?P<facet>[^\/]+)/?$', views.PaginatedFacetView.as_view(
        redirect='authority_search',
        form_class=forms.FacetListSearchForm,
        model=models.Authority,
        facetclasses=FACETS),
            name='authority_facets'),
    url(r'^/?$', views.PortalListView.as_view(
        model=models.Authority,
        template_name="authority_list.html",
        ), name='authority_list'),
    # Crud Actions
    url(r'^create/?$', 
            user_passes_test(permissions.is_staff)(
                views.AuthorityEditView.as_view()), name='authority_create'),
    url(r'^edit/(?P<slug>[-\w]+)/?$',
            user_passes_test(permissions.is_staff)(
                views.AuthorityEditView.as_view()), name='authority_edit'),
    url(r'^delete/(?P<slug>[-\w]+)/?$', 
            user_passes_test(permissions.is_staff)(
                views.AuthorityDeleteView.as_view()), name='authority_delete'),
    url(r'^history/(?P<slug>[-\w]+)/?$', views.PortalHistoryView.as_view(
            model=models.Authority,
        ), name='authority_history'),
    url(r'^restore/(?P<slug>[-\w]+)/v/(?P<revision>\d+)/?$', views.PortalRestoreView.as_view(
            model=models.Authority,
        ), name='authority_restore'),
    url(r'^(?P<slug>[-\w]+)/v/(?P<revision>\d+)/?$', views.PortalRevisionView.as_view(
            model=models.Authority,
            template_name="authority_revision.html"
        ), name='authority_revision'),
    url(r'^diff/(?P<slug>[-\w]+)/?$', views.PortalRevisionDiffView.as_view(
            model=models.Authority,
            template_name="authority_diff.html",
        ), name='authority_diff'),
    
    # these catch-all item must be at the bottom
    url(r'^(?P<slug>[-\w]+)/?$', views.PortalDetailView.as_view(
            model=models.Authority,
            template_name="authority_detail.html"
        ), name='authority_detail'),
    url(r'^(?P<slug>[-\w]+)/collections/?$', 
            views.ListCollectionsView.as_view(
                template_name="collection_list.html",
                related_item_model=models.Authority,
                related_item_attr="creator",
            ), name='authority_collections'),
)

