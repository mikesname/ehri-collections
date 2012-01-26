"""Archival description model."""

import datetime

from django.db import models

from ehriportal.repositories.models import Repository


class Description(models.Model):
    """Model representing an archival description."""
    LODS = ()
    ENTITY_TYPES = ()

    identifier = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    lod = models.CharField(max_length=255, choices=LODS)
    type_of_entity = models.CharField(max_length=255, choices=ENTITY_TYPES)
    language = models.CharField(max_length=20, default="en")
    language_of_description = models.CharField(max_length=20, default="en")
    created_on = models.DateTimeField(editable=False)
    updated_on = models.DateTimeField(editable=False, null=True, blank=True)

    # optional translatable text fields
    repository = models.ForeignKey(Repository)
    access_conditions = models.TextField(null=True, blank=True)
    accruals = models.TextField(null=True, blank=True)
    acquisition = models.TextField(null=True, blank=True)
    alternate_title = models.TextField(null=True, blank=True)
    appraisal = models.TextField(null=True, blank=True)
    archival_history = models.TextField(null=True, blank=True)
    arrangement = models.TextField(null=True, blank=True)
    edition = models.TextField(null=True, blank=True)
    extent_and_medium = models.TextField(null=True, blank=True)
    finding_aids = models.TextField(null=True, blank=True)
    institution_responsible_identifier = models.TextField(null=True, blank=True)
    location_of_copies = models.TextField(null=True, blank=True)
    location_of_originals = models.TextField(null=True, blank=True)
    physical_characteristics = models.TextField(null=True, blank=True)
    related_units_of_description = models.TextField(null=True, blank=True)
    reproduction_conditions = models.TextField(null=True, blank=True)
    revision_history = models.TextField(null=True, blank=True)
    rules = models.TextField(null=True, blank=True)
    scope_and_content = models.TextField(null=True, blank=True)
    sources = models.TextField(null=True, blank=True)

    def save(self):
        if not self.id:
            self.created_on = datetime.datetime.now()
        else:
            self.updated_on = datetime.datetime.now()
        super(Description, self).save()

    @property
    def other_names(self):
        """Get a list of other names."""
        return [on.name for on in self.othername_set.all()]

class OtherName(models.Model):
    name = models.CharField(max_length=255)
    description = models.ForeignKey(Description)


