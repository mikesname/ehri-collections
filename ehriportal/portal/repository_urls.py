from django.conf.urls.defaults import *
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

urlpatterns = patterns('',
    #url(r'^/?$', object_list, listinfo, name='repo_list'),
    url(r'^/?$', FacetedSearchView(
        form_class=FacetedSearchForm, searchqueryset=sqs,
        template="portal/repository_search.html"), name='repo_search'),
    url(r'^(?P<slug>[-\w]+)/?$', object_detail, viewinfo, name='repo_detail'),
)

