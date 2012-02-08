"""Suggestions model."""

import datetime
from django.db import models


class SuggestionType(models.Model):
    """Category for suggestions."""
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class Suggestion(models.Model):
    """Suggestion class."""
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    types = models.ManyToManyField(SuggestionType)
    text = models.TextField()
    created_on = models.DateTimeField(editable=False)
    updated_on = models.DateTimeField(editable=False, null=True, blank=True)

    def type_list(self):
        """Shortcut for fetching a list of types."""
        return [t.name for t in self.types.all()]

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = datetime.datetime.now()
        else:
            self.updated_on = datetime.datetime.now()
        super(Suggestion, self).save(*args, **kwargs)

    def __unicode__(self):
        text = self.text[:17]
        if len(text) != self.text:
            text += "..."
        return "%s: '%s'" % (self.name, text)

    @models.permalink
    def get_absolute_url(self):
        return ('suggestion_detail', [self.id])



