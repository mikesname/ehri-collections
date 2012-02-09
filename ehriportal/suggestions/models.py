"""Suggestions model."""

import datetime
from django.db import models
import jsonfield


GRAB_META = [
        "HTTP_USER_AGENT",
        "HTTP_HOST",
        "REMOTE_HOST",
        "HTTP_ACCEPT",
        "HTTP_REFERER",
        "REMOTE_ADDR",
        "CONTEXT_TYPE",
        "HTTP_ACCEPT_LANGUAGE",
        "QUERY_STRING",
]

def get_suggestion_meta(request):
    """Return a dictionary of interesting things about
    a request that we want to store with the suggestion,
    since it might give some useful extra context."""
    return dict([(k, v) for k, v in request.META.iteritems() \
            if k in GRAB_META])


class Suggestion(models.Model):
    """Suggestion class."""
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    text = models.TextField()
    meta = jsonfield.JSONField(null=True)
    created_on = models.DateTimeField(editable=False)
    updated_on = models.DateTimeField(editable=False, null=True, blank=True)

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



