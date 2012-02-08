"""Portal search forms."""

from django import forms
from django.utils.translation import ugettext_lazy as _

from haystack.forms import FacetedSearchForm
from portal import views

class SearchForm(forms.Form):
    q = forms.CharField(required=False, label=_('Search'))
    

class PortalSearchForm(FacetedSearchForm):
    """Specialisation of FacetedSearchForm for portal."""
    def search(self):
        """Override the standard faceted search form."""
        # NOTE: We purposely do NOT call the base class, because it
        # includes problematic behaviour WRT quoting facet query strings
        sqs = super(FacetedSearchForm, self).search()

        # We need to process each facet to ensure that the field name and the
        # value are quoted correctly and separately:
        for facet in self.selected_facets:
            if ":" not in facet:
                continue
            field, value = facet.split(":", 1)
            # FIXME: This part overrides the base class so that
            # facet values that match a date math string are NOT
            # quoted, which screws them up.  This is unfortunate 
            # and a better way needs to be found
            if value:
                keyval = u'%s:"%s"' % (field, sqs.query.clean(value))
                if views.DATEMATH.match(value):
                    keyval = u'%s:%s' % (field, value)
                sqs = sqs.narrow(keyval)
        return sqs

    def no_query_found(self):
        """Show all results when not given a query."""
        sqs = self.searchqueryset.all()
        if self.load_all:
            sqs = sqs.load_all()
        return sqs

