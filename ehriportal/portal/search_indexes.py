import datetime
from haystack.indexes import *
from haystack import site
from ehriportal.portal.models import Repository, Collection
from ehriportal.portal import utils

from incf.countryutils import data as countrydata


class RepositoryIndex(SearchIndex):
    name = CharField(model_attr='name', default=True, boost=1.1)
    slug = CharField(model_attr='slug', indexed=False, stored=True)
    description = CharField(model_attr='general_context', null=True)
    other_names = MultiValueField(model_attr='other_names')
    country = CharField(model_attr='country', faceted=True, null=True, stored=True)
    text = CharField(document=True, use_template=True, stored=False)
    pub_date = DateTimeField(model_attr='created_on')
    suggestions = CharField()

    def prepare(self, obj):
        prepared_data = super(RepositoryIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Repository.objects.filter(created_on__lte=datetime.datetime.now())


class MultiValueIntegerField(MultiValueField):
    """Multi-valued Int field."""
    field_type = "integer"

class FacetMultiValueIntegerField(FacetMultiValueField):
    """Multi-valued Int field."""
    field_type = "integer"


class MultiValueDateField(MultiValueField):
    """Multi-valued date field."""
    field_type = "date"

class FacetMultiValueDateField(FacetMultiValueField):
    """Multi-valued date field."""
    field_type = "date"


class CollectionIndex(SearchIndex):
    name = CharField(model_attr='name', default=True, boost=1.1)
    slug = CharField(model_attr='slug', indexed=False, stored=True)
    description = CharField(model_attr='scope_and_content', null=True)
    other_names = MultiValueField(model_attr='other_names')
    repository = CharField(model_attr='repository__name')
    repository_uri = CharField(model_attr='repository__get_absolute_url', stored=True, indexed=False)
    repository_other_names = MultiValueField(model_attr='repository__other_names')
    location_of_materials = CharField(model_attr='repository__country', faceted=True, null=True)
    languages = MultiValueField(model_attr='languages', faceted=True)
    tags = MultiValueField(model_attr='tag_list', faceted=True)
    start_date = DateField(model_attr='start_date', faceted=True, null=True)
    years = MultiValueIntegerField(model_attr='date_range', faceted=True, null=True)
    dates = MultiValueDateField(model_attr='date_range', null=True)
    dates_exact = FacetMultiValueDateField(model_attr='date_range', null=True)
    date_range = CharField(model_attr='date_range_string', stored=True, indexed=False, null=True)
    end_date = DateField(model_attr='end_date', faceted=True, null=True)
    languages_of_description = MultiValueField(model_attr='languages_of_description', 
            faceted=True)
    text = CharField(document=True, use_template=True, stored=False)
    #ngram = EdgeNgramField(use_template=True, template_name="search/indexes/portal/collection_text.txt",
    #        stored=False)
    pub_date = DateTimeField(model_attr='created_on')
    suggestions = CharField()

    def prepare(self, obj):
        prepared_data = super(CollectionIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data

    def prepare_languages(self, desc):
        """Get pretty name for language."""
        return [utils.language_name_from_code(l) for l in desc.languages]

    def prepare_languages_of_description(self, desc):
        """Get pretty name for language of description."""
        return [utils.language_name_from_code(l) for l in desc.languages_of_description]

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Collection.objects.filter(created_on__lte=datetime.datetime.now())

    def prepare_years(self, desc):
        """Turn dates into an integer for year."""
        return [d.year for d in desc.date_range]


site.register(Collection, CollectionIndex)
site.register(Repository, RepositoryIndex)
