import datetime
from haystack.indexes import *
from haystack import site
from ehriportal.repositories.models import Repository


class RepositoryIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    pub_date = DateTimeField(model_attr='created_on')

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Repository.objects.filter(created_on__lte=datetime.datetime.now())


site.register(Repository, RepositoryIndex)
