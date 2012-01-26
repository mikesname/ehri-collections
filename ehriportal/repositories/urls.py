from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from ehriportal.repositories import views, models

from haystack.views import FacetedSearchView
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet

sqs = SearchQuerySet().models(models.Repository).facet('country')

urlpatterns = patterns('',
    url(r'^/?$', views.FacetedSearchView(
        form_class=FacetedSearchForm, searchqueryset=sqs,
        template="repositories/search.html"), name='repos'),
)
