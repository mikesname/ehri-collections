"""Archival description model."""

from django.db import models

from ehriportal.repositories.models import Repository
from ehriportal.archival_resource.models import ArchivalResource

class Description(ArchivalResource):
    """Model representing an archival description."""
    LODS = ()
    ENTITY_TYPES = ()

    translatable_fields = (
        ("access_conditions", "TODO: Help text"),
        ("accruals", "TODO: Help text"),
        ("acquisition", "TODO: Help text"),
        ("alternate_title", "TODO: Help text"),
        ("appraisal", "TODO: Help text"),
        ("archival_history", "TODO: Help text"),
        ("arrangement", "TODO: Help text"),
        ("edition", "TODO: Help text"),
        ("extent_and_medium", "TODO: Help text"),
        ("finding_aids", "TODO: Help text"),
        ("institution_responsible_identifier", "TODO: Help text"),
        ("location_of_copies", "TODO: Help text"),
        ("location_of_originals", "TODO: Help text"),
        ("physical_characteristics", "TODO: Help text"),
        ("related_units_of_description", "TODO: Help text"),
        ("reproduction_conditions", "TODO: Help text"),
        ("revision_history", "TODO: Help text"),
        ("rules", "TODO: Help text"),
        ("scope_and_content", "TODO: Help text"),
        ("sources", "TODO: Help text"),
    )

    repository = models.ForeignKey(Repository)

    @property
    def languages_of_description(self):
        return self.get_property("languages_of_description")
