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
from django.utils.encoding import smart_str, force_unicode

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
        super_new = super(ResourceType, cls).__new__
         # Abstract class: abstract attribute should not be inherited.
        if attrs.pop("abstract", None) or not attrs.get("autoregister", True):
            return super_new(cls, name, bases, attrs)
        for fname, vname, help in attrs.get("translatable_fields", []):
            super_new.add_to_class(fname, nodeprop.String(name=vname, nullable=True))
        return super_new(cls, name, bases, attrs)



class ResourceBase(djbulbs.models.Model, models.EntityUrlMixin):
    """Mixin for resources holding common properties."""
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

    def __repr__(self):
        return u"<%s: %s>" % (self.__class__.__name__, self.name)

    @property
    def resource_type(self):
        return self._meta.verbose_name

    @property
    def published(self):
        return self.publication_status == self.PUBLISHED

    def _create(self, _data, kwds):
        kwds["created_on"] = kwds.get("created_on", current_datetime())
        # get the slug from the name
        kwds["slug"] = self._get_slug(kwds["name"])
        return super(ResourceBase, self)._create(_data, kwds)

    def _update(self, _id, _data, kwds):
        kwds["updated_on"] = kwds.get("updated_on", current_datetime())
        return super(ResourceBase, self)._update(_id, _data, kwds)

    def save(self, *args, **kwargs):
        if not self.created_on:
            raise Exception("Unable to save an object created with its own __init__()")
        else:
            self.updated_on = current_datetime()
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

    def get_repository(self):
        try:
            return self.outE(HeldBy.label).next().inV()
        except StopIteration:
            return

    def set_repository(self, repo):
        try:
            rel = self.outE(HeldBy.label).next().eid
            djbulbs.graph.heldBy.delete(rel)
        except StopIteration:
            # this should mean there is no existing repository
            pass
        if repo is not None:
            djbulbs.graph.heldBy.create(self, repo)

    repository = property(get_repository, set_repository)

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

