import datetime
from haystack.indexes import *
from haystack import site
from ehriportal.descriptions.models import Description
from ehriportal.descriptions import utils


class DescriptionIndex(SearchIndex):
    name = CharField(model_attr='name', default=True)
    other_names = MultiValueField(model_attr='other_names')
    repository = CharField(model_attr='repository__name')
    language = CharField(model_attr='language', null=True, faceted=True)
    language_of_description = CharField(model_attr='language_of_description', 
            null=True, faceted=True)
    text = CharField(document=True, use_template=True, stored=False)
    pub_date = DateTimeField(model_attr='created_on')

    def prepare_language(self, desc):
        """Get pretty name for language."""
        return utils.language_name_from_code(desc.language)

    def prepare_language_of_description(self, desc):
        """Get pretty name for language of description."""
        return utils.language_name_from_code(desc.language_of_description)

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Description.objects.filter(created_on__lte=datetime.datetime.now())


site.register(Description, DescriptionIndex)
