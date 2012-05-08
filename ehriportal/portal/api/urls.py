"""
URLs for accessing resources via the API.
"""

from django.conf.urls.defaults import *
from tastypie import api
from portal.api import resources


v1_api = api.Api(api_name="v1")
v1_api.register(resources.ResourceResource())
v1_api.register(resources.RepositoryResource())
v1_api.register(resources.CollectionResource())
v1_api.register(resources.AuthorityResource())
v1_api.register(resources.FuzzyDateResource())

urlpatterns = patterns('',
   url(r'^', include(v1_api.urls)),
)
