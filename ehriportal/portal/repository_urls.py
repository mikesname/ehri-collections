from django.conf.urls.defaults import *
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.list_detail import object_detail, object_list
from django.contrib.auth.decorators import login_required
from ehriportal.portal import views, models

from haystack.views import FacetedSearchView
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet

sqs = SearchQuerySet().models(models.Repository).facet('country')

listinfo = dict(
        queryset=models.Repository.objects.all(),
        paginate_by=10
)

viewinfo = dict(
        queryset=models.Repository.objects.all(),
)


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
    url(r'^/?$', FacetedSearchView(
        form_class=FacetedSearchForm, searchqueryset=sqs,
        template="portal/repository_search.html"), name='repo_search'),
    url(r'^(?P<slug>[-\w]+)/?$', object_detail, viewinfo, name='repo_detail'),
    url(r'^(?P<slug>[-\w]+)/collections/?$', 
            ListCollectionsView.as_view(), name='repo_collections'),
)

