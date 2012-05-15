"""
Portal entities as Bulb Graph nodes.
"""

import os
import re
import datetime
import json

from django.conf import settings
from django.utils.translation import ugettext as _

from portal import utils

from bulbs import model, property as nodeprop
from bulbs.utils import current_datetime
from bulbs import neo4jserver

# FIXME: Do away with this global somehow
GRAPH = neo4jserver.Graph() # FIXME: Handle non-default config


class HeldBy(model.Relationship):
    label = "heldBy"
GRAPH.add_proxy(HeldBy.label, HeldBy)


class CreatedBy(model.Relationship):
    label = "createdBy"
GRAPH.add_proxy(CreatedBy.label, CreatedBy)




class ResourceType(model.ModelMeta):
    """Metaclass for archival resources. Don't fear the magic.
    All this does is instantiate models.TextField attributes
    on subclasses based on their translatable_fields tuple."""
    def __new__(cls, name, bases, attrs):
        new = super(ResourceType, cls).__new__
         # Abstract class: abstract attribute should not be inherited.
        if attrs.pop("abstract", None) or not attrs.get("autoregister", True):
            return new(cls, name, bases, attrs)
        for fname, vname, help in attrs.get("translatable_fields", []):
            attrs[fname] = nodeprop.String(name=vname, nullable=True)

        newtype = new(cls, name, bases, attrs)
        # create a proxy in the graph for this type
        if attrs.get("element_type"):
            GRAPH.add_proxy(attrs.get("element_type"), newtype)
        return newtype

    def __repr__(cls):
        return "<class %s>" % cls.__name__


class Repository(model.Node):
    """Repository."""
    __metaclass__ = ResourceType
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

    name = nodeprop.String(name=_("Name"), nullable=False, unique=True)
    level_of_description = nodeprop.Integer(name=_("Level of Description"))
    type_of_entity = nodeprop.Integer(name=_("Type of Entity"))
    languages = nodeprop.List(name=_("Language(s)"))
    scripts = nodeprop.List(name=_("Script(s)"))

    @property
    def collections(self):
        """Get all collections related by the heldBy edge."""
        for edge in self.inE(HeldBy.label):
            yield edge.outV()

    def natural_key(self):
        return (self.name,)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)

    def __unicode__(self):
        return self.name


class Collection(model.Node):
    """Model representing an archival description."""
    __metaclass__ = ResourceType
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

    name = nodeprop.String(name=_("Title"), nullable=False, unique=True)
    identifier = nodeprop.String(indexed=True, name=_("Local Identifier"), nullable=False)
    level_of_description = nodeprop.Integer(name=_("Level of Description"))
    languages = nodeprop.List(name=_("Language(s)"))
    scripts = nodeprop.List(name=_("Script(s)"))
    languages_of_description = nodeprop.List(name=_("Language(s) of Description"))
    scripts_of_description = nodeprop.List(name=_("Script(s) of Description"))

    @property
    def repository(self):
        try:
            return self.outE(HeldBy.label).next().inV()
        except StopIteration:
            return

    # FIXME: Can't make this a property setter (as would be nice)
    # because the Bulbs node model overrides __setattr__.
    def set_repository(self, repo):
        try:
            rel = self.outE(HeldBy.label).next().eid
            GRAPH.heldBy.delete(rel)
        except StopIteration:
            # this should mean there is no existing repository
            pass
        GRAPH.heldBy.create(self, repo)

    def natural_key(self):
        return (self.name,)


class Authority(model.Node):
    """Model representing an archival authority."""
    __metaclass__ = ResourceType
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

    name = nodeprop.String(name=_("Authorized Form of Name"), nullable=False)
    level_of_detail = nodeprop.Integer(name=_("Level of Description"))
    type_of_entity = nodeprop.Integer(name=_("Type of Entity"),
            nullable=False)
    languages = nodeprop.List(name=_("Language(s)"))
    scripts = nodeprop.List(name=_("Script(s)"))

    def natural_key(self):
        return (self.name,)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)

    def __unicode__(self):
        return self.name


