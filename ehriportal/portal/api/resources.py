"""
Tastypie resources for notable models.
"""


from tastypie import resources
from portal import models


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





