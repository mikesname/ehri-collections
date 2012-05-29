"""
Portal entities as Bulb Graph nodes.
"""

import os
import sys
import re
import datetime
import json

from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _

from portal import utils, terms, models

import djbulbs
from djbulbs.models import nodeprop
from djbulbs.manager import GraphManager

current_datetime = datetime.datetime.now

class HeldBy(djbulbs.models.Relationship):
    label = "heldBy"
djbulbs.graph.add_proxy(HeldBy.label, HeldBy)


class CreatedBy(djbulbs.models.Relationship):
    label = "createdBy"
djbulbs.graph.add_proxy(CreatedBy.label, CreatedBy)


class MentionedIn(djbulbs.models.Relationship):
    label = "mentionedIn"
djbulbs.graph.add_proxy(MentionedIn.label, MentionedIn)


class ResourceBaseType(djbulbs.models.ModelType):
    """Metaclass for resource types. Don't fear the magic.
    All this does is instantiate models.TextField attributes
    on subclasses based on their translatable_fields tuple."""
    def __new__(cls, name, bases, attrs):
        super_new = super(ResourceBaseType, cls).__new__
         # Abstract class: abstract attribute should not be inherited.
        new_class = super_new(cls, name, bases, attrs)
        if attrs.pop("abstract", None) or not attrs.get("autoregister", True):
            return new_class 
        for fname, vname, help in attrs.get("translatable_fields", []):
            new_class.add_to_class(fname, nodeprop.String(name=vname, nullable=True))
        return new_class



class ResourceBase(djbulbs.models.Model, models.EntityUrlMixin):
    """Mixin for resources holding common properties."""
    __metaclass__ = ResourceBaseType
    # Publication status enum
    DRAFT, PUBLISHED = range(2)
    PUB_STATUS = (
            (DRAFT, _("Draft")),
            (PUBLISHED, _("Published")),
    )

    name = nodeprop.String(name=_("Name"), unique=True, indexed=True, nullable=False)
    slug = nodeprop.String(name=_("Slug"), unique=True, indexed=True, nullable=False)
    created_on = nodeprop.DateTime(name=_("Date Created"), nullable=False)
    updated_on = nodeprop.DateTime(name=_("Date Updated"), nullable=True)
    publication_status = nodeprop.Integer(name=_("Publication Status"),
            default=DRAFT, indexed=True, nullable=True)

    def _get_slug(self, name):
        proxy = getattr(djbulbs.graph, self.element_type)
        initial = 2
        base = slugify(name)
        potential = base
        while True:
            ires = proxy.index.lookup(slug=potential)
            if len(list(ires)) == 0:
                break
            potential = u"%s-%d" % (base, initial)
            initial += 1
        return potential

    @property
    def resource_type(self):
        return self._meta.verbose_name

    @property
    def published(self):
        return self.publication_status == self.PUBLISHED

    def save(self, *args, **kwargs):
        if not hasattr(self, "eid"):
            # Grotesque hacks to get around Bulbs difficulties. Because
            # of the convoluted way that item._data gets populated, and
            # the distinction between stored and regular properties
            self._data["slug"] = self.slug = self._get_slug(self._data["name"])
            self._data["created_on"] = self.created_on = current_datetime()
        else:
            self._data["updated_on"] = self.updated_on = current_datetime()
        return super(ResourceBase, self).save(*args, **kwargs)

    def to_dict(self):
        """Serialize to dictionary."""
        return self.data()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.slug)



class Repository(ResourceBase):
    """Repository."""
    element_type = "repository"
    level_of_description = nodeprop.Integer(name=_("Level of Description"))
    type_of_entity = nodeprop.Integer(name=_("Type of Entity"))
        
    access_conditions = nodeprop.String(name=_("Access Conditions"), nullable=True)
    buildings = nodeprop.String(name=_("Buildings"), nullable=True)
    collecting_policies = nodeprop.String(name=_("Collecting Policies"), nullable=True)
    dates_of_existence = nodeprop.String(name=_("Dates of Existence"), nullable=True)
    disabled_access = nodeprop.String(name=_("Disabled Access"), nullable=True)
    finding_aids = nodeprop.String(name=_("Finding Aids"), nullable=True)
    functions = nodeprop.String(name=_("Functions"), nullable=True)
    general_context = nodeprop.String(name=_("General Context"), nullable=True)
    geocultural_context = nodeprop.String(name=_("Geocultural Context"), nullable=True)
    history = nodeprop.String(name=_("History"), nullable=True)
    holdings = nodeprop.String(name=_("Holdings"), nullable=True)
    internal_structures = nodeprop.String(name=_("Internal Structures"), nullable=True)
    legal_status = nodeprop.String(name=_("Legal Status"), nullable=True)
    maintenance_notes = nodeprop.String(name=_("Maintenance Notes"), nullable=True)
    mandates = nodeprop.String(name=_("Mandates"), nullable=True)
    opening_times = nodeprop.String(name=_("Opening Times"), nullable=True)
    places = nodeprop.String(name=_("Places"), nullable=True)
    reproduction_services = nodeprop.String(name=_("Reproduction Services"), nullable=True)
    research_services = nodeprop.String(name=_("Research Services"), nullable=True)
    rules = nodeprop.String(name=_("Rules"), nullable=True)
    sources = nodeprop.String(name=_("Sources"), nullable=True)

    languages = nodeprop.List(name=_("Language(s)"))
    scripts = nodeprop.List(name=_("Script(s)"))

    objects = GraphManager()

    @property
    def collection_set(self):
        qs = Collection.objects.all()
        return qs.start_from("g.v(%d).inE('heldBy').outV" % self.eid)

    @property
    def collections(self):
        """Get all collections related by the heldBy edge."""
        for edge in self.inE(HeldBy.label):
            yield edge.outV()

    def natural_key(self):
        return (self.name,)
djbulbs.graph.add_proxy(Repository.element_type, Repository)


class Collection(ResourceBase):
    """Model representing an archival description."""
    element_type = "collection"
    translatable_fields = ()

    objects = GraphManager()

    identifier = nodeprop.String(indexed=True, name=_("Local Identifier"), nullable=False)
    level_of_description = nodeprop.Integer(name=_("Level of Description"))

    access_conditions = nodeprop.String(name=_("Access Conditions"), nullable=True)
    accruals = nodeprop.String(name=_("Accruals"), nullable=True)
    acquisition = nodeprop.String(name=_("Immediate source of acquisition or transfer"), nullable=True)
    alternate_title = nodeprop.String(name=_("Alternate Title"), nullable=True)
    appraisal = nodeprop.String(name=_("Appraisal"), nullable=True)
    archival_history = nodeprop.String(name=_("Archival History"), nullable=True)
    arrangement = nodeprop.String(name=_("Arrangement"), nullable=True)
    edition = nodeprop.String(name=_("Edition"), nullable=True)
    extent_and_medium = nodeprop.String(name=_("Extent and Medium"), nullable=True)
    finding_aids = nodeprop.String(name=_("Finding Aids"), nullable=True)
    institution_responsible_identifier = nodeprop.String(name=_("Institution Responsible Identifier"), nullable=True)
    location_of_copies = nodeprop.String(name=_("Location of Copies"), nullable=True)
    location_of_originals = nodeprop.String(name=_("Location of Originals"), nullable=True)
    notes = nodeprop.String(name=_("Notes"), nullable=True)
    physical_characteristics = nodeprop.String(name=_("Physical Characteristics"), nullable=True)
    related_units_of_description = nodeprop.String(name=_("Related Units of Description"), nullable=True)
    reproduction_conditions = nodeprop.String(name=_("Reproduction Conditions"), nullable=True)
    revision_history = nodeprop.String(name=_("Revision History"), nullable=True)
    rules = nodeprop.String(name=_("Rules"), nullable=True)
    scope_and_content = nodeprop.String(name=_("Scope and Content"), nullable=True)
    sources = nodeprop.String(name=_("Sources"), nullable=True)

    languages = nodeprop.List(name=_("Language(s)"))
    scripts = nodeprop.List(name=_("Script(s)"))
    languages_of_description = nodeprop.List(name=_("Language(s) of Description"))
    scripts_of_description = nodeprop.List(name=_("Script(s) of Description"))

    creator = djbulbs.models.SingleRelationField(CreatedBy)
    repository = djbulbs.models.SingleRelationField(HeldBy)


    def natural_key(self):
        return (self.name,)
djbulbs.graph.add_proxy(Collection.element_type, Collection)


class Authority(ResourceBase):
    """Model representing an archival authority."""
    element_type = "authority"
    @property
    def collection_set(self):
        qs = Collection.objects.all()
        return qs.start_from("g.v(%d).inE('createdBy').outV" % self.eid)

    @property
    def mentioned_set(self):
        qs = Collection.objects.all()
        return qs.start_from("g.v(%d).inE('mentionedIn').outV" % self.eid)

    identifier = nodeprop.String(indexed=True, name=_("Local Identifier"), nullable=False)
    level_of_description = nodeprop.Integer(name=_("Level of Description"))
    type_of_entity = nodeprop.Integer(name=_("Type of Entity"),
            nullable=False)
    
    dates_of_existence = nodeprop.String(name=_("Dates of Existence"), nullable=True)
    functions = nodeprop.String(name=_("Functions"), nullable=True)
    general_context = nodeprop.String(name=_("General Context"), nullable=True)
    history = nodeprop.String(name=_("History"), nullable=True)
    institution_responsible_identifier = nodeprop.String(name=_("Institution Responsible Identifier"), nullable=True)
    internal_structures = nodeprop.String(name=_("Internal Structures"), nullable=True)
    legal_status = nodeprop.String(name=_("Legal Status"), nullable=True)
    mandates = nodeprop.String(name=_("Mandates"), nullable=True)
    places = nodeprop.String(name=_("Places"), nullable=True)
    revision_history = nodeprop.String(name=_("Revision History"), nullable=True)
    sources = nodeprop.String(name=_("Sources"), nullable=True)

    languages = nodeprop.List(name=_("Language(s)"))
    scripts = nodeprop.List(name=_("Script(s)"))

    objects = GraphManager()

    def natural_key(self):
        return (self.name,)
djbulbs.graph.add_proxy(Authority.element_type, Authority)

