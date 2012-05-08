"""
Tastypie resources for notable models.
"""


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




# Yes, the name is all sorts of wrong
class ResourceResource(resources.ModelResource):
    class Meta:
        queryset = models.Resource.objects.all()

class RepositoryResource(resources.ModelResource):
    class Meta:
        queryset = models.Repository.objects.all()

class CollectionResource(resources.ModelResource):
    class Meta:
        queryset = models.Collection.objects.all()

class AuthorityResource(resources.ModelResource):
    class Meta:
        queryset = models.Authority.objects.all()

class FuzzyDateResource(resources.ModelResource):
    class Meta:
        queryset = models.FuzzyDate.objects.all()





