"""
Django shim for Bulbs models.
"""


from django.db.models.options import Options

from bulbs import model, property as nodeprop
from bulbs.utils import current_datetime, initialize_element, \
        initialize_elements
from bulbs import neo4jserver



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


class Model(model.Node, models.EntityUrlMixin):
    __metaclass__ = ResourceType
    __mode__ = model.STRICT

    class DoesNotExist(ObjectDoesNotExist):
        pass

    class MultipleObjectsReturned(MultipleObjectsReturned):
        pass

    def __init__(self, client, **kwargs):
        super(Model, self).__init__(client)
        self.__dict__.update(**kwargs)

    def __str__(self):
        if hasattr(self, '__unicode__'):
            return force_unicode(self).encode('utf-8')
        return '%s object' % self.__class__.__name__



