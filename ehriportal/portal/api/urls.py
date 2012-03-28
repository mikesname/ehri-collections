"""
URLs for accessing resources via the API.
"""

from django.conf.urls.defaults import *
from piston import resource
from portal.api import handlers


authority_resource = resource.Resource(handlers.AuthorityHandler)
collection_resource = resource.Resource(handlers.CollectionHandler)
contact_resource = resource.Resource(handlers.ContactHandler)
place_resource = resource.Resource(handlers.PlaceHandler)
repository_resource = resource.Resource(handlers.RepositoryHandler)


urlpatterns = patterns('',
   url(r'^authorities/(?P<id>\d+)$', authority_resource),
   url(r'^authorities/(?P<slug>[-\w]+)$', authority_resource),
   url(r'^authorities/?$', authority_resource),
   url(r'^collections/(?P<id>\d+)$', collection_resource),
   url(r'^collections/(?P<slug>[-\w]+)$', collection_resource),
   url(r'^collections/?$', collection_resource),
   url(r'^contact/(?P<id>\d+)$', contact_resource),
   url(r'^contact/?$', contact_resource),
   url(r'^places/(?P<id>\d+)$', place_resource),
   url(r'^places/?$', place_resource),
   url(r'^repositories/(?P<id>\d+)$', repository_resource),
   url(r'^repositories/(?P<slug>[-\w]+)$', repository_resource),
   url(r'^repositories/?$', repository_resource),
)
