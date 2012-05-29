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

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.slug)



class Repository(ResourceBase):
    """Repository."""
    element_type = "repository"
    translatable_fields = (
        ("access_conditions", "Access Conditions", "TODO: Help text"),
        ("buildings", "Buildings", "TODO: Help text"),
        ("collecting_policies", "Collecting Policies", "TODO: Help text"),
        ("dates_of_existence", "Dates of Existence", "TODO: Help text"),
        ("disabled_access", "Disabled Access", "TODO: Help text"),
        ("finding_aids", "Finding Aids", "TODO: Help text"),
        ("functions", "Functions", "TODO: Help text"),
        ("general_context", "General Context", "TODO: Help text"),
        ("geocultural_context", "Geocultural Context", "TODO: Help text"),
        ("history", "History", "TODO: Help text"),
        ("holdings", "Holdings", "TODO: Help text"),
        ("internal_structures", "Internal Structures", "TODO: Help text"),
        ("legal_status", "Legal Status", "TODO: Help text"),
        ("maintenance_notes", "Maintenance Notes", "TODO: Help text"),
        ("mandates", "Mandates", "TODO: Help text"),
        ("opening_times", "Opening Times", "TODO: Help text"),
        ("places", "Places", "TODO: Help text"),
        ("reproduction_services", "Reproduction Services", "TODO: Help text"),
        ("research_services", "Research Services", "TODO: Help text"),
        ("rules", "Rules", "TODO: Help text"),
        ("sources", "Sources", "TODO: Help text"),
    )

    lod = nodeprop.Integer(name=_("Level of Description"))
    type_of_entity = nodeprop.Integer(name=_("Type of Entity"))
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
    translatable_fields = (
        ("access_conditions", "Access Conditions", "TODO: Help text"),
        ("accruals", "Accruals", "TODO: Help text"),
        ("acquisition", "Immediate source of acquisition or transfer", "TODO: Help text"),
        ("alternate_title", "Alternate Title", "TODO: Help text"),
        ("appraisal", "Appraisal", "TODO: Help text"),
        ("archival_history", "Archival History", "TODO: Help text"),
        ("arrangement", "Arrangement", "TODO: Help text"),
        ("edition", "Edition", "TODO: Help text"),
        ("extent_and_medium", "Extent and Medium", "TODO: Help text"),
        ("finding_aids", "Finding Aids", "TODO: Help text"),
        ("institution_responsible_identifier", "Institution Responsible Identifier", "TODO: Help text"),
        ("location_of_copies", "Location of Copies", "TODO: Help text"),
        ("location_of_originals", "Location of Originals", "TODO: Help text"),
        ("notes", _("Notes"), "TODO: Help text"),
        ("physical_characteristics", "Physical Characteristics", "TODO: Help text"),
        ("related_units_of_description", "Related Units of Description", "TODO: Help text"),
        ("reproduction_conditions", "Reproduction Conditions", "TODO: Help text"),
        ("revision_history", "Revision History", "TODO: Help text"),
        ("rules", "Rules", "TODO: Help text"),
        ("scope_and_content", "Scope and Content", "TODO: Help text"),
        ("sources", "Sources", "TODO: Help text"),
    )

    objects = GraphManager()

    identifier = nodeprop.String(indexed=True, name=_("Local Identifier"), nullable=False)
    lod = nodeprop.Integer(name=_("Level of Description"))
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
    translatable_fields = (
        ("dates_of_existence", "Dates of Existence", "TODO: Help text"),
        ("functions", "Functions", "TODO: Help text"),
        ("general_context", "General Context", "TODO: Help text"),
        ("history", "History", "TODO: Help text"),
        ("institution_responsible_identifier", "Institution Responsible Identifier", "TODO: Help text"),
        ("internal_structures", "Internal Structures", "TODO: Help text"),
        ("legal_status", "Legal Status", "TODO: Help text"),
        ("mandates", "Mandates", "TODO: Help text"),
        ("places", "Places", "TODO: Help text"),
        ("revision_history", "Revision History", "TODO: Help text"),
        ("sources", "Sources", "TODO: Help text"),
    )

    @property
    def collection_set(self):
        qs = Collection.objects.all()
        return qs.start_from("g.v(%d).inE('createdBy').outV" % self.eid)

    @property
    def mentioned_set(self):
        qs = Collection.objects.all()
        return qs.start_from("g.v(%d).inE('mentionedIn').outV" % self.eid)

    lod = nodeprop.Integer(name=_("Level of Description"))
    type_of_entity = nodeprop.Integer(name=_("Type of Entity"),
            nullable=False)
    languages = nodeprop.List(name=_("Language(s)"))
    scripts = nodeprop.List(name=_("Script(s)"))

    objects = GraphManager()

    def natural_key(self):
        return (self.name,)
djbulbs.graph.add_proxy(Authority.element_type, Authority)

