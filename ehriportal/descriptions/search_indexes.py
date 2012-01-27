import datetime
from haystack.indexes import *
from haystack import site
from ehriportal.descriptions.models import Description
from ehriportal.descriptions import utils


class DescriptionIndex(SearchIndex):
    name = CharField(model_attr='name', default=True)
    other_names = MultiValueField(model_attr='other_names')
    repository = CharField(model_attr='repository__name')
    languages = MultiValueField(model_attr='languages', faceted=True)
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
        return Description.objects.filter(created_on__lte=datetime.datetime.now())


site.register(Description, DescriptionIndex)
