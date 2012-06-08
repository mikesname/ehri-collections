"""
Django shim for Bulbs models.
"""

import sys

from django.db.models.options import Options
from django.db.models import signals
from django.utils.encoding import smart_str, force_unicode
from django.core.exceptions import (ObjectDoesNotExist, 
            MultipleObjectsReturned)

from bulbs import model, property as nodeprop
from bulbs.utils import current_datetime, initialize_element, \
        initialize_elements
from bulbs.neo4jserver import batch
from bulbs.neo4jserver.client import gremlin_path

from . import graph as GRAPH, manager


# just alias relationship for now
class Relationship(model.Relationship):
    """Alias for Bulbs relationship."""


class SingleRelationField(object):
    def __init__(self, relation):
        self.relation = relation

    def contribute_to_class(cls, model, name):
        cls.model = model
        model._relations[name] = cls
        rel = cls.relation
        def lookup_func(self):
            cached = self._relation_cache.get(name)
            if cached is not None:
                return cached
            # we can do this with bulbs directly, saving some hassle
            try:
                self._relation_cache[name] = self.outE(rel.label).next().inV()
            except StopIteration:
                pass
            return self._relation_cache.get(name)

        def setter_func(self, other):
            self._pending_relations[rel.label] = other
            self._relation_cache[name] = other
        setattr(model, name, property(lookup_func, setter_func))
        


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
        
        # HACK! Simulate making a pk field in Options called eid
        class PkField:
            attname = name = GRAPH.config.id_var
        new_class._meta.pk = PkField()

        # add a lookup for relations
        new_class.add_to_class('_relations', dict())

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


class Model(model.Node):
    __metaclass__ = ModelType
    __mode__ = model.STRICT

    class DoesNotExist(ObjectDoesNotExist):
        pass

    class MultipleObjectsReturned(MultipleObjectsReturned):
        pass

    def __init__(self, client=None, **kwargs):
        signals.pre_init.send(sender=self.__class__, args=[], kwargs=kwargs)
        if client is None:
            client = GRAPH.client
        super(Model, self).__init__(client)

        self._relation_cache = {}
        self._pending_relations = {}
        for key, cls in self._relations.items():
            relinst = kwargs.pop(key, None)
            if relinst is not None:
                self._pending_relations[cls.relation.label] = relinst
                self._relation_cache[key] = relinst
        self._data.update(**kwargs)

    @property
    def pk(self):
        return self._get_pk_val()

    def _get_pk_val(self, meta=None):
        if meta is None:
            meta = self._meta
        return getattr(self, meta.pk.attname, None)

    def save(self, *args, **kwargs):
        signals.pre_save.send(sender=self.__class__, instance=self, raw=False, using=None,
                                  update_fields=None)
        creating = self._get_pk_val() is None

        # This is how we would do it if it were currently possible
        # create and set relationships in a batch, but it isn't
        # because we need the pk to set relationships
        #index_name = self.get_index_name(self._client.config)
        #keys = self.get_index_keys()
        #data = self._get_property_data()
        #params = dict(data=data,index_name=index_name,keys=keys)
        #script = self._client.scripts.get("create_indexed_vertex")
        #if updating:
        #    script = self._client.scripts.get("update_indexed_vertex")
        #    params["_id"] = self.pk
        #neobatch.add_message("POST", gremlin_path, dict(script=script, params=params))

        if creating:
            self._create(self._data, {})
        else:
            super(Model, self).save()

        # start of batch request...
        neobatch = batch.Neo4jBatchRequest(self._client.request.config, 
                    self._client.request.content_type)
        # set relationships...
        for relname, instance in self._pending_relations.items():
            script = self._client.scripts.get("set_single_relation")
            params = dict(outV=self.pk, inV=instance.pk if instance else None, label=relname)
            args = ["POST", gremlin_path, dict(script=script, params=params)]
            neobatch.add_message(*args)
        neobatch.send()

        # reset pending relations so they're not set again on save...
        self._pending_relations = {}

        signals.post_save.send(sender=self.__class__, instance=self, created=creating,
                                   update_fields=None, raw=False, using=None)

    def __unicode__(self):
        return u"<%s: %d>" % (self.__class__, self._get_pk_val())

    def __str__(self):
        if hasattr(self, '__unicode__'):
            return force_unicode(self).encode('utf-8')
        return '%s object' % self.__class__.__name__

    def _get_pk_val(self):
        if hasattr(self, self._meta.pk.attname):
            return getattr(self, self._meta.pk.attname)

    def delete(self):
        assert self._get_pk_val() is not None, "%s object can't be deleted because its %s attribute is set to None." % (self._meta.object_name, self._meta.pk.attname)
        signals.pre_delete.send(sender=self.__class__, instance=self, using=None)
        # TODO: Add more error checking here...
        # Bulbs should throw an exception if anything goes badly wrong
        GRAPH.vertices.delete(self._get_pk_val())
        signals.post_delete.send(sender=self.__class__, instance=self, using=None)



