"""
Tastypie resources for notable models.
"""

from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from tastypie import resources, serializers
from portal import models

# Unused/unfinished collection exporter/importer that
# supports EAD.
class CollectionSerializer(serializers.Serializer):
    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'ead']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'ead': 'application/xml',
    }

    # NOTE: This is an incredibly naive implementation
    # meant only as a proof of concept
    def to_ead(self, data, options):
        options = options or {}
        data = self.to_simple(data, options)

    def from_ead(self, data, options):
        pass


class SlugResource(resources.ModelResource):
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<slug>[\w\d_.-]+)/$" % self._meta.resource_name, 
                    self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def get_resource_uri(self, bundle):
        return reverse("api_dispatch_detail", kwargs={
            'resource_name': self._meta.resource_name,
            'slug': bundle.data['slug'],
            'api_name': 'v1', # FIXME: Hard-coded api name...
        })
    def dehydrate_languages(self, bundle):
        return bundle.obj.languages

    def dehydrate_scripts(self, bundle):
        return bundle.obj.scripts

    def dehydrate_languages_of_description(self, bundle):
        return bundle.obj.languages_of_description

    def dehydrate_scripts_of_description(self, bundle):
        return bundle.obj.scripts_of_description



# Yes, the name is all sorts of wrong
class ResourceResource(resources.ModelResource):
    class Meta:
        queryset = models.Resource.objects.all()

class RepositoryResource(SlugResource):
    class Meta:
        queryset = models.Repository.objects.all()

class CollectionResource(SlugResource):
    class Meta:
        queryset = models.Collection.objects.all()

class AuthorityResource(SlugResource):
    class Meta:
        queryset = models.Authority.objects.all()

class FuzzyDateResource(resources.ModelResource):
    class Meta:
        queryset = models.FuzzyDate.objects.all()





