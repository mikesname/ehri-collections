"""
Repository model.
"""

from django.db import models

class Repository(models.Model):
    """Repository."""
    ENTITY_TYPES=()
    LOD = ()

    identifier = models.CharField(max_length=255)
    authorized_form_of_name = models.CharField(max_length=255)
    lod = models.CharField(max_length=255, choices=LOD)
    type_of_entity = models.CharField(max_length=255, choices=ENTITY_TYPES)
    dates_of_existence = models.TextField(null=True, blank=True)
    history = models.TextField(null=True, blank=True)
    places = models.TextField(null=True, blank=True)
    legal_status = models.TextField(null=True, blank=True)
    functions = models.TextField(null=True, blank=True)
    mandates = models.TextField(null=True, blank=True)
    internal_structures = models.TextField(null=True, blank=True)
    general_context = models.TextField(null=True, blank=True)
    rules_conventions = models.TextField(null=True, blank=True)
    sources = models.TextField(null=True, blank=True)
    maintenance_notes = models.TextField(null=True, blank=True)


    def __unicode__(self):
        return self.identifier

class OtherName(models.Model):
    name = models.CharField(max_length=255)
    repository = models.ForeignKey(Repository, related_name="other_names")



