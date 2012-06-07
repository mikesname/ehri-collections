"""
Django shim for Bulbs models.
"""


from django.db.models.manager import Manager, ManagerDescriptor

from .query import GraphQuerySet

class GraphManager(Manager):
    """Mock manager for graph models."""
    def get_query_set(self):
        return GraphQuerySet(self.model)

    def contribute_to_class(self, model, name):
        self.model = model
        mandesc = ManagerDescriptor(self)
        setattr(model, name, mandesc)
        if not hasattr(model, "_default_manager"):
            setattr(model, "_default_manager", mandesc)

    def create(self, **kwargs):
        qs = self.get_query_set()
        return super(GraphManager, self).create(**kwargs)

    def outgoing(self, *args, **kwargs):
        return self.get_query_set().outgoing(*args, **kwargs)
    
    def incoming(self, *args, **kwargs):
        return self.get_query_set().incoming(*args, **kwargs)


