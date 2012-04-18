"""Haystack 2.0 search index bindings."""

import datetime
from haystack import indexes
from portal import models, utils


class MultiValueIntegerField(indexes.MultiValueField):
    """Multi-valued Int field."""
    field_type = "integer"

class FacetMultiValueIntegerField(indexes.FacetMultiValueField):
    """Multi-valued Int field."""
    field_type = "integer"


class MultiValueDateField(indexes.MultiValueField):
    """Multi-valued date field."""
    field_type = "date"

class FacetMultiValueDateField(indexes.FacetMultiValueField):
    """Multi-valued date field."""
    field_type = "date"


class RepositoryIndex(indexes.SearchIndex, indexes.Indexable):
    name = indexes.CharField(model_attr='name', default=True, boost=1.1)
    slug = indexes.CharField(model_attr='slug', indexed=False, stored=True)
    description = indexes.CharField(model_attr='general_context', null=True)
    other_names = indexes.MultiValueField(model_attr='other_names')
    address = indexes.CharField(model_attr='primary_contact', null=True, stored=True, indexed=False)
    country = indexes.CharField(faceted=True, null=True, stored=True)
    location = indexes.LocationField(null=True, faceted=True, stored=True)
    text = indexes.CharField(document=True, use_template=True, stored=False)
    pub_date = indexes.DateTimeField(model_attr='created_on')
    suggestions = indexes.CharField()

    def get_model(self):
        return models.Repository

    def prepare(self, obj):
        prepared_data = super(RepositoryIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data

    def prepare_country(self, desc):
        return desc.country

    def prepare_address(self, desc):
        contact = desc.primary_contact
        if contact:
            return contact.format()

    def prepare_location(self, desc):
        try:
            place = desc.place_set.all()[0]
        except IndexError:
            return
        return "%s,%s" % (place.point.x, place.point.y)

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created_on__lte=datetime.datetime.now())


class AuthorityIndex(indexes.SearchIndex, indexes.Indexable):
    name = indexes.CharField(model_attr='name', default=True, boost=1.1)
    slug = indexes.CharField(model_attr='slug', indexed=False, stored=True)
    history = indexes.CharField(model_attr='history', null=True, stored=True)
    general_context = indexes.CharField(model_attr='general_context', null=True)
    other_names = indexes.MultiValueField(model_attr='other_names')
    type_of_entity = indexes.CharField(model_attr='type_of_entity', faceted=True, stored=True)
    text = indexes.CharField(document=True, use_template=True, stored=False)
    pub_date = indexes.DateTimeField(model_attr='created_on')
    suggestions = indexes.CharField()

    def get_model(self):
        return models.Authority

    def prepare(self, obj):
        prepared_data = super(AuthorityIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created_on__lte=datetime.datetime.now())


class CollectionIndex(indexes.SearchIndex, indexes.Indexable):
    name = indexes.CharField(model_attr='name', default=True, boost=1.1)
    slug = indexes.CharField(model_attr='slug', indexed=False, stored=True)
    description = indexes.CharField(model_attr='scope_and_content', null=True)
    other_names = indexes.MultiValueField(model_attr='other_names')
    repository = indexes.CharField(model_attr='repository__name')
    repository_uri = indexes.CharField(model_attr='repository__get_absolute_url', stored=True, indexed=False)
    repository_other_names = indexes.MultiValueField(model_attr='repository__other_names')
    location_of_materials = indexes.CharField(model_attr='repository__country', faceted=True, null=True)
    languages = indexes.MultiValueField(model_attr='languages', faceted=True)
    tags = indexes.MultiValueField(model_attr='tag_list', faceted=True)
    start_date = indexes.DateField(model_attr='start_date', faceted=True, null=True)
    years = MultiValueIntegerField(model_attr='date_range', faceted=True, null=True)
    dates = MultiValueDateField(model_attr='date_range', null=True)
    dates_exact = FacetMultiValueDateField(model_attr='date_range', null=True)
    date_range = indexes.CharField(model_attr='date_range_string', stored=True, indexed=False, null=True)
    end_date = indexes.DateField(model_attr='end_date', faceted=True, null=True)
    languages_of_description = indexes.MultiValueField(model_attr='languages_of_description', 
            faceted=True)
    text = indexes.CharField(document=True, use_template=True, stored=False)
    #ngram = indexes.EdgeNgramField(use_template=True, template_name="search/indexes/portal/collection_text.txt",
    #        stored=False)
    pub_date = indexes.DateTimeField(model_attr='created_on')
    suggestions = indexes.CharField()

    def get_model(self):
        return models.Collection

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
        return self.get_model().objects.filter(created_on__lte=datetime.datetime.now())

    def prepare_years(self, desc):
        """Turn dates into an integer for year."""
        return [d.year for d in desc.date_range]

