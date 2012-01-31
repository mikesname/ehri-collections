import datetime
from haystack.indexes import *
from haystack import site
from ehriportal.portal.models import Repository, Collection
from ehriportal.portal import utils

from incf.countryutils import data as countrydata


class RepositoryIndex(SearchIndex):
    name = CharField(model_attr='name', default=True)
    description = CharField(model_attr='general_context', null=True)
    other_names = MultiValueField(model_attr='other_names')
    country = CharField(model_attr='country', faceted=True, null=True)
    text = CharField(document=True, use_template=True, stored=False)
    pub_date = DateTimeField(model_attr='created_on')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Repository.objects.filter(created_on__lte=datetime.datetime.now())


class CollectionIndex(SearchIndex):
    name = CharField(model_attr='name', default=True)
    description = CharField(model_attr='scope_and_content', null=True)
    other_names = MultiValueField(model_attr='other_names')
    repository = CharField(model_attr='repository__name')
    location_of_materials = CharField(model_attr='repository__country', faceted=True, null=True)
    languages = MultiValueField(model_attr='languages', faceted=True)
    tags = MultiValueField(model_attr='tag_list', faceted=True)
    languages_of_description = MultiValueField(model_attr='languages_of_description', 
            faceted=True)
    text = CharField(document=True, use_template=True, stored=False)
    pub_date = DateTimeField(model_attr='created_on')

    def prepare_languages(self, desc):
        """Get pretty name for language."""
        return [utils.language_name_from_code(l) for l in desc.languages]

    def prepare_languages_of_description(self, desc):
        """Get pretty name for language of description."""
        return [utils.language_name_from_code(l) for l in desc.languages_of_description]

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Collection.objects.filter(created_on__lte=datetime.datetime.now())


site.register(Collection, CollectionIndex)
site.register(Repository, RepositoryIndex)
