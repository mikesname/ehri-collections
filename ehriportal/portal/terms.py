"""
Definitions for some taxonomy terms.
"""
from django.utils.translation import ugettext as _

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


