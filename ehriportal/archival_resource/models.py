"""Archival resource model.  Base class for Repositories and Descriptions."""

import datetime

from django.db import models
from django.db.models.base import ModelBase

from autoslug import AutoSlugField


class ArchivalResourceType(ModelBase):
    """Metaclass for archival resources. Don't fear the magic.
    All this does is instantiate models.TextField attributes
    on subclasses based on their translatable_fields tuple."""
    def __new__(cls, name, bases, attrs):
        new = super(ArchivalResourceType, cls).__new__
         # Abstract class: abstract attribute should not be inherited.
        if attrs.pop("abstract", None) or not attrs.get("autoregister", True):
            return new(cls, name, bases, attrs)
        for fname, help in attrs.get("translatable_fields", []):
            attrs[fname] = models.TextField(null=True, blank=True, help_text=help)
        return new(cls, name, bases, attrs)

    def __repr__(cls):
        return "<class %s>" % cls.__name__


class ArchivalResource(models.Model):
    """Archival resource."""
    __metaclass__ = ArchivalResourceType
    #abstract = True
    translatable_fields = ()

    ENTITY_TYPES=()
    LOD = ()

    identifier = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", unique=True)
    type = models.CharField(max_length=255)
    lod = models.CharField(max_length=255, choices=LOD)
    type_of_entity = models.CharField(max_length=255, choices=ENTITY_TYPES)
    created_on = models.DateTimeField(editable=False)
    updated_on = models.DateTimeField(editable=False, null=True, blank=True)

    def save(self):
        if not self.slug:
            self.created_on = datetime.datetime.now()
        else:
            self.updated_on = datetime.datetime.now()
        if not self.type:
            self.type = self.__class__.__name__
        super(ArchivalResource, self).save()

    @property
    def other_names(self):
        """Get a list of other names."""
        return [on.name for on in self.othername_set.all()]

    @property
    def properties(self):
        """Get a list of property key/value pairs."""
        return [(p.name, p.value) for p in self.property_set.all()]

    @property
    def languages(self):
        """Short cut for fetching language properties."""
        return self.get_property("language")

    @property
    def scripts(self):
        """Short cut for fetching language properties."""
        return self.get_property("script")

    def get_property(self, propname):
        """Fetch a list of properties with the given name."""
        return [p[1] for p in self.properties if p[0] == propname]

    def set_property(self, name, value):
        """Set a property.  This does NOT imply overwriting 
        existing ones, since multiple properties can have the
        same name, i.e. language: [en, de]."""
        self.property_set.add(Property(resource=self, name=name, value=value))

    def delete_property(self, name, withval=None):
        """Delete a property with the given name and (optionally)
        the given value."""
        qset = self.property_set.filter(name=name)
        if withval is not None:
            qset = self.property_set.filter(value=value)
        qset.delete()

    def __unicode__(self):
        return u"<%s: %s>" % (self.type, self.identifier)


class OtherName(models.Model):
    name = models.CharField(max_length=255)
    resource = models.ForeignKey(ArchivalResource)


class Property(models.Model):
    """Generic property for resources."""
    resource = models.ForeignKey(ArchivalResource)
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
