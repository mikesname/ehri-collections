import datetime
from haystack.indexes import *
from haystack import site
from ehriportal.repositories.models import Repository

from incf.countryutils import data as countrydata


class RepositoryIndex(SearchIndex):
    name = CharField(model_attr='name', default=True)
    other_names = MultiValueField(model_attr='other_names')
    country = CharField(model_attr='country', faceted=True, null=True)
    text = CharField(document=True, use_template=True, stored=False)
    pub_date = DateTimeField(model_attr='created_on')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Repository.objects.filter(created_on__lte=datetime.datetime.now())


site.register(Repository, RepositoryIndex)
