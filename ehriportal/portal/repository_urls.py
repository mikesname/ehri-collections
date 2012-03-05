from django.conf.urls.defaults import *
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.create_update import update_object
from django.contrib.auth.decorators import login_required

from portal import views, forms, models
from portal.haystack_util import FacetClass

from haystack.query import SearchQuerySet

FACETS = [
    FacetClass(
        "country",
        "Country",
    )
]

listinfo = dict(
        queryset=models.Repository.objects.all().order_by("name"),
        paginate_by=20
)

viewinfo = dict(
        queryset=models.Repository.objects.all(),
)

class RepoEditForm(ModelForm):
    class Meta:
        model = models.Repository


class ListCollectionsView(ListView):
    paginate_by = 20
    def get_queryset(self, *args, **kwargs):
        self.repository = get_object_or_404(
                models.Repository, slug=self.kwargs["slug"])
        return models.Collection.objects.filter(repository=self.repository)

    def get_context_data(self, *args, **kwargs):
        extra = super(ListCollectionsView, self).get_context_data(*args, **kwargs)
        extra["repository"] = self.repository
        return extra



urlpatterns = patterns('',
    #url(r'^/?$', object_list, listinfo, name='repo_list'),
    url(r'^search/?$', views.PortalSearchListView.as_view(
        model=models.Repository,
        facetclasses=FACETS,
        template_name="repository_search.html"), name='repo_search'),
    url(r'^map/?$', views.PortalSearchListView.as_view(
        facetclasses=FACETS,
        form_class=forms.MapSearchForm,
        template_name="repository_map.html"), name='repo_map'),
    url(r'^search/(?P<facet>[^\/]+)/?$', views.PaginatedFacetView.as_view(
        redirect='repo_search',
        form_class=forms.FacetListSearchForm,
        model=models.Repository,
        facetclasses=FACETS),
            name='collection_facets'),
    url(r'^/?$', object_list, listinfo, name='repo_list'),
    url(r'^(?P<slug>[-\w]+)/?$', object_detail, dict(
            queryset=models.Repository.objects.all(),
            template_name="repository_detail.html"
        ), name='repo_detail'),
    url(r'^(?P<slug>[-\w]+)/edit/?$', update_object, dict(
            form_class=RepoEditForm
        ), name='repo_edit'),
    url(r'^(?P<slug>[-\w]+)/collections/?$', 
            ListCollectionsView.as_view(
                template_name="collection_list.html"    
            ), name='repo_collections'),
)

