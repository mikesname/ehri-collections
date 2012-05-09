"""
Tastypie resources for notable models.
"""

from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from tastypie import fields, resources, serializers, bundle
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

    def get_resource_uri(self, bundle_or_obj):
        """Build the URI using the slug instead of the default PK."""
        kwargs = {
            'resource_name': self._meta.resource_name,
        }
        if isinstance(bundle_or_obj, bundle.Bundle):
            kwargs['slug'] = bundle_or_obj.obj.slug
        else:
            kwargs['slug'] = bundle_or_obj.slug
        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name
        return self._build_reverse_url("api_dispatch_detail", kwargs=kwargs)

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

class DateResource(resources.ModelResource):
    class Meta:
        queryset = models.FuzzyDate.objects.all()

class OtherNameResource(resources.ModelResource):
    class Meta:
        queryset = models.OtherName.objects.all()

class RepositoryResource(SlugResource):
    other_names = fields.ListField()
    class Meta:
        queryset = models.Repository.objects.all()
    
    def dehydrate_other_names(self, bundle):
        return bundle.obj.other_names

class CollectionResource(SlugResource):
    repository = fields.ForeignKey(RepositoryResource, 'repository')
    other_names = fields.ListField()
    dates = fields.CharField()
    class Meta:
        queryset = models.Collection.objects.select_related().all()

    def dehydrate_dates(self, bundle):
        return bundle.obj.date_range_string

    def dehydrate_other_names(self, bundle):
        return bundle.obj.other_names

class AuthorityResource(SlugResource):
    other_names = fields.ListField()
    class Meta:
        queryset = models.Authority.objects.all()

    def dehydrate_other_names(self, bundle):
        return bundle.obj.other_names




