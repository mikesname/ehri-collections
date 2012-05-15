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

from bulbs import model, property
from bulbs.utils import current_datetime

# Publication status enum
DRAFT, PUBLISHED = range(2)
PUB_STATUS = (
        (DRAFT, _("Draft")),
        (PUBLISHED, _("Published")),
)

FULL, PARTIAL, MINIMAL = range(3)
LEVELS_OF_DETAIL = (
    (FULL, _("Full")),
    (PARTIAL, _("Partial")),
    (MINIMAL, _("Minimal")),
)

CORPORATE_BODY, FAMILY, PERSON = range(3)
AUTHORITY_TYPES = (
    (CORPORATE_BODY, _("Corporate Body")),
    (FAMILY, _("Family")),
    (PERSON, _("Person")),
)

COLLECTION, FONDS, SUBFONDS, SERIES, SUBSERIES, FILE, ITEM = range(7)
LEVELS_OF_DESCRIPTION = (
    (COLLECTION, _("Collection")),
    (FONDS, _("Fonds")),
    (SUBFONDS, _("Sub-fonds")),
    (SERIES, _("Series")),
    (SUBSERIES, _("Sub-series")),
    (FILE, _("File")),
    (ITEM, _("Item")),
)

INTERNATIONAL, NATIONAL, REGIONAL, PROVINCIAL, COMMUNITY, \
        RELIGIOUS, UNIVERSITY, MUNICIPAL, ABORIGINAL, EDUCATIONAL = range(10)
ENTITY_TYPES = (
    (INTERNATIONAL, _("International")),
    (NATIONAL, _("National")),
    (REGIONAL, _("Regional")),
    (PROVINCIAL, _("Provincial")),
    (COMMUNITY, _("Community")),
    # ... TODO
)


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
            attrs[fname] = property.String(name=vname, nullable=True)
        return new(cls, name, bases, attrs)

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

    name = property.String(name=_("Name"), nullable=False)
    level_of_description = property.Integer(name=_("Level of Description"))
    type_of_entity = property.Integer(name=_("Type of Entity"))
    languages = property.List(name=_("Language(s)"))
    scripts = property.List(name=_("Script(s)"))

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

    name = property.String(name=_("Title"), nullable=False)
    identifier = property.String(indexed=True, name=_("Local Identifier"), nullable=False)
    level_of_description = property.Integer(name=_("Level of Description"))
    languages = property.List(name=_("Language(s)"))
    scripts = property.List(name=_("Script(s)"))
    languages_of_description = property.List(name=_("Language(s) of Description"))
    scripts_of_description = property.List(name=_("Script(s) of Description"))

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

    name = property.String(name=_("Authorized Form of Name"), nullable=False)
    level_of_detail = property.Integer(name=_("Level of Description"))
    type_of_entity = property.Integer(name=_("Type of Entity"),
            nullable=False)
    languages = property.List(name=_("Language(s)"))
    scripts = property.List(name=_("Script(s)"))

    def natural_key(self):
        return (self.name,)

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.name)

    def __unicode__(self):
        return self.name


