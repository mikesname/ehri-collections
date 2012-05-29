from django.conf.urls.defaults import *
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import update_object
from django.contrib.auth.decorators import login_required, user_passes_test

from portal import views, forms, utils, models, nodes, permissions
from portal.haystack_util import FacetClass

from haystack.query import SearchQuerySet

FACETS = [
    FacetClass(
        "country",
        "Country",
        renderfn=utils.country_name_from_code,
    )
]



urlpatterns = patterns('',
    url(r'^search/?$', views.PortalSearchListView.as_view(
        model=models.Repository,
        facetclasses=FACETS,
        template_name="repository_search.html"), name='repository_search'),
    url(r'^search/(?P<facet>[^\/]+)/?$', views.PaginatedFacetView.as_view(
        redirect='repository_search',
        form_class=forms.FacetListSearchForm,
        model=nodes.Repository,
        facetclasses=FACETS),
            name='collection_facets'),
    url(r'^/?$', views.PortalListView.as_view(
        model=nodes.Repository,
        template_name="repository_list.html",
        ), name='repository_list'),

    # Crud Actions
    url(r'^create/?$', 
            user_passes_test(permissions.is_staff)(
                views.RepositoryEditView.as_view(model=nodes.Repository)), name='repository_create'),
    url(r'^edit/(?P<slug>[-\w]+)/?$',
            user_passes_test(permissions.is_staff)(
                views.RepositoryEditView.as_view(model=nodes.Repository)), name='repository_edit'),
    url(r'^delete/(?P<slug>[-\w]+)/?$', 
            user_passes_test(permissions.is_staff)(
                views.RepositoryDeleteView.as_view(model=nodes.Repository)), name='repository_delete'),
    url(r'^(?P<slug>[-\w]+)/collections/create/?$', 
            views.RepositoryCollectionCreateView.as_view(model=nodes.Repository), 
                name='repository_collection_create'),
    
    # these catch-all item must be at the bottom
    url(r'^(?P<slug>[-\w]+)/?$', views.PortalCollectionHolderDetailView.as_view(
            model=nodes.Repository,
            template_name="repository_detail.html"
        ), name='repository_detail'),
    url(r'^(?P<slug>[-\w]+)/collections/?$', 
            views.ListCollectionsView.as_view(
                template_name="collection_list.html",
                related_item_model=nodes.Repository,
                related_item_attr="repository",
            ), name='repository_collections'),
)

