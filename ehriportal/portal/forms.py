"""Portal search forms."""

import string
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis import geos
from django.forms.models import modelformset_factory, inlineformset_factory

from haystack.forms import EmptySearchQuerySet

from portal import models


def parse_point(pointstr):
    print "PARSING", pointstr
    """Parse a GEOS point from a two-float string."""
    try:
        y, x = string.split(pointstr, ",")
    except IndexError:
        return None
    try:
        return geos.Point(float(x), float(y))
    except ValueError:
        return None


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

class PortalAllSearchForm(PortalSearchForm):
    def no_query_found(self):
        return EmptySearchQuerySet()



class MapSearchForm(PortalSearchForm):
    type = forms.ChoiceField(label=_('Type'), choices=(("Repository", "Repository"),
            ("Collection", "Collection")))
    ne = forms.CharField(required=False, label=_('North East'),
            widget=forms.HiddenInput())
    sw = forms.CharField(required=False, label=_('South West'),
            widget=forms.HiddenInput())

    def no_query_found(self):
        """Show no results for a map search."""
        return EmptySearchQuerySet()

    def filter(self, sqs):
        """Filter a search set with geo-bounds."""
        model = getattr(models, self.cleaned_data["type"])
        sqs = sqs.models(model)
        if self.cleaned_data["ne"] and self.cleaned_data["sw"]:
            botlft = parse_point(self.cleaned_data["sw"])
            toprgt = parse_point(self.cleaned_data["ne"])
            if botlft and toprgt:
                sqs = sqs.within("location", botlft, toprgt)
        return super(MapSearchForm, self).filter(sqs)


class FacetListSearchForm(PortalSearchForm):
    """Extension of the search form with another field for
    the order in which facets are sorted.  Since we can't do
    this natively with Haystack, we have to hack it ourselves.
    """
    sort = forms.ChoiceField(required=False, 
            choices=(("count",_("Count")), ("name", _("Name"))))


class FuzzyDateForm(forms.ModelForm):
    class Meta:
        model = models.FuzzyDate
        fields = ("start_date", "end_date",)
        widgets = {
                "start_date": forms.TextInput(attrs={'class':'input-small', 'placeholder': 'Start Date'}),
                "end_date": forms.TextInput(attrs={'class':'input-small', 'placeholder': 'End Date'}),
        }


class CollectionEditForm(forms.ModelForm):
    class Meta:
        model = models.Collection


class RepositoryEditForm(forms.ModelForm):
    class Meta:
        model = models.Repository


class AuthorityEditForm(forms.ModelForm):
    class Meta:
        model = models.Authority


def propertyformset_factory(topclass, propname):
    propcls = models.propertyproxy_factory(propname)
    return inlineformset_factory(
            topclass, propcls, fields=("value",), extra=1)


DateFormSet = inlineformset_factory(models.Collection, models.FuzzyDate,
        form=FuzzyDateForm, extra=1)


OtherNameFormSet = inlineformset_factory(models.Collection, models.OtherFormOfName,
        exclude=("type",), extra=1)


ParallelNameFormSet = inlineformset_factory(models.Collection, models.ParallelFormOfName,
        exclude=("type",), extra=1)


ContactFormSet = inlineformset_factory(models.Repository, models.Contact,
        extra=1)


