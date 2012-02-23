"""Portal search forms."""

from django import forms
from django.utils.translation import ugettext_lazy as _

from haystack.forms import EmptySearchQuerySet


class PortalSearchForm(forms.Form):
    q = forms.CharField(required=False, label=_('Search'))

    def filter(self, sqs):
        """Filter a search queryset."""
        self.sqs = sqs
        if not self.cleaned_data["q"]:
            return self.no_query_found()
        return sqs.auto_query(self.cleaned_data["q"])

    def no_query_found(self):
        return self.sqs


class MapSearchForm(PortalSearchForm):
    def no_query_found(self):
        """Show no results for a map search."""
        return EmptySearchQuerySet()


class FacetListSearchForm(PortalSearchForm):
    """Extension of the search form with another field for
    the order in which facets are sorted.  Since we can't do
    this natively with Haystack, we have to hack it ourselves.
    """
    sort = forms.ChoiceField(required=False, 
            choices=(("count",_("Count")), ("name", _("Name"))))



