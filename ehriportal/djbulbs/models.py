"""
Django shim for Bulbs models.
"""

import sys

from django.db.models.options import Options
from django.utils.encoding import smart_str, force_unicode

from bulbs import model, property as nodeprop
from bulbs.utils import current_datetime, initialize_element, \
        initialize_elements

from . import graph as GRAPH, manager


# just alias relationship for now
class Relationship(model.Relationship):
    """Alias for Bulbs relationship."""


class SingleRelationField(object):
    def __init__(self, relation):
        self.relation = relation

    def contribute_to_class(self, model, name):
        self.model = model
        model._relations[name] = self
        rel = self.relation
        def lookup_func(self):
            cached = model._relation_cache.get(name)
            if cached is not None:
                return cached
            # we can do with with bulbs, saving some hassle
            try:
                model._relation_cache[name] = self.outE(rel.label).next().inV()
            except StopIteration:
                pass
            return model._relation_cache.get(name)
        setattr(model, name, property(lookup_func))
        


class ModelType(model.ModelMeta):
    """Metaclass for DjBulbs models."""
    def __new__(cls, name, bases, attrs):
        super_new = super(ModelType, cls).__new__
        parents = [b for b in bases if isinstance(b, ModelType)]
        if not parents:
            # If this isn't a subclass of Model, don't do anything special.
            return super_new(cls, name, bases, attrs)

        # Create the class.
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        attr_meta = attrs.pop('Meta', None)
        abstract = getattr(attr_meta, 'abstract', False)
        if not attr_meta:
            meta = getattr(new_class, 'Meta', None)
        else:
            meta = attr_meta
        base_meta = getattr(new_class, '_meta', None)

        if getattr(meta, 'app_label', None) is None:
            # Figure out the app_label by looking one level up.
            # For 'django.contrib.sites.models', this would be 'sites'.
            model_module = sys.modules[new_class.__module__]
            kwargs = {"app_label": model_module.__name__.split('.')[-2]}
        else:
            kwargs = {}

        new_class.add_to_class('_meta', Options(meta, **kwargs))

        # add a lookup for relations
        new_class.add_to_class('_relations', dict())
        new_class.add_to_class('_relation_cache', dict())

         # Abstract class: abstract attribute should not be inherited.
        if attrs.pop("abstract", None) or not attrs.get("autoregister", True):
            return super_new(cls, name, bases, attrs)
        
        # Add other attributes
        for name, obj in attrs.items():
            new_class.add_to_class(name, obj)

        return new_class

    # Try and make some Django magic happy
    def add_to_class(cls, name, value):
        if hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)

    def __repr__(cls):
        return "<class %s>" % cls.__name__


from django.core.exceptions import (ObjectDoesNotExist, 
            MultipleObjectsReturned)


class Model(model.Node):
    __metaclass__ = ModelType
    __mode__ = model.STRICT

    class DoesNotExist(ObjectDoesNotExist):
        pass

    class MultipleObjectsReturned(MultipleObjectsReturned):
        pass

    def __init__(self, client=None, **kwargs):
        if client is None:
            client = GRAPH.client
        super(Model, self).__init__(client)
        self._data.update(**kwargs)

    def save(self, *args, **kwargs):
        if not hasattr(self, "eid"):
            self._create(self._data, {})
        else:
            super(Model, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"<%s: %d>" % (self.__class__, self.eid)

    def __str__(self):
        if hasattr(self, '__unicode__'):
            return force_unicode(self).encode('utf-8')
        return '%s object' % self.__class__.__name__



