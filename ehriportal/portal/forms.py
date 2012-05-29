"""Portal search forms."""

import string
from django import forms
from django.contrib.admin import widgets
from django.utils import translation
from django.utils.translation import ugettext as _
from django.contrib.gis import geos
from django.forms.models import modelformset_factory, inlineformset_factory

from jsonfield.forms import JSONFormField
from haystack.forms import EmptySearchQuerySet

from portal import models, terms, data, utils


def parse_point(pointstr):
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
    ENTITIES = [models.Repository, models.Collection, models.Authority]
    SORTFIELDS = (
            ("", _("Relevance")),
            ("name", _("Title/Name")),
            ("publication_date", _("Publication Date")),
            ("django_ct", _("Type")),
    )
    q = forms.CharField(required=False, label=_('Search'))
    sort = forms.ChoiceField(required=False, choices=SORTFIELDS, label=_("Order By"))

    def filter(self, sqs):
        """Filter a search queryset."""
        self.sqs = sqs
        if self.cleaned_data["sort"]:
            self.sqs = self.sqs.order_by(self.cleaned_data["sort"])
        if not self.cleaned_data["q"]:
            return self.no_query_found()
        return sqs.auto_query(self.cleaned_data["q"])

    def no_query_found(self):
        return self.sqs

class PortalAllSearchForm(PortalSearchForm):
    """Form representing the whole collection."""
   # def no_query_found(self):
   #     return EmptySearchQuerySet()


class LanguageSelectWidget(forms.SelectMultiple):
    choices = utils.language_choices()
    def __init__(self, *args, **kwargs):
        super(LanguageSelectWidget, self).__init__(*args, **kwargs)


class ScriptSelectWidget(forms.SelectMultiple):
    choices = utils.script_choices()


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


class LanguageSelectFormField(forms.MultipleChoiceField):
    def __init__(self, *args, **kwargs):
        super(LanguageSelectFormField, self).__init__(*args, **kwargs)
        self.widget = forms.SelectMultiple(choices=utils.language_choices())


class ScriptSelectFormField(forms.MultipleChoiceField):
    def __init__(self, *args, **kwargs):
        super(ScriptSelectFormField, self).__init__(*args, **kwargs)
        self.widget = forms.SelectMultiple(choices=utils.script_choices())


class FuzzyDateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        attrs={
            'class':'input-small',
            'placeholder': 'Start Date'
        }
        super(FuzzyDateForm, self).__init__(*args, **kwargs)
        self.fields["start_date"].widget = widgets.AdminDateWidget(attrs=attrs)
        self.fields["end_date"].widget = widgets.AdminDateWidget(attrs=attrs)

    class Meta:
        model = models.FuzzyDate
        fields = ("start_date", "end_date",)


class OtherNameForm(forms.ModelForm):
    class Meta:
        fields = ("name",)
        widgets = {
                "name": forms.TextInput(attrs={'placeholder': _("Type another name here...")}),
        }

class PortalEntityForm(forms.Form):
    # extra (non-model) field for revision comment
    publication_status = forms.ChoiceField(label=_("Publication Status"), 
                choices=terms.PUBLICATION_STATUS, help_text=_("Status of this item with regards to "
                                                            "public visibility."))
    revision_comment = forms.CharField(required=False, widget=forms.TextInput(attrs={
                "placeholder": _("Summary of changes (optional)"),
            }))

class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact


class FreeTextField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(FreeTextField, self).__init__(*args, **kwargs)
        self.widget = forms.Textarea()


class CollectionEditForm(PortalEntityForm):
    """Form representing an ISAD(G) collection entry (minus its relations
    to other entities such as the repository and creator.)"""
    identifier = forms.CharField(label=_("Identifier"), help_text=_(""))
    name = forms.CharField(label=_("Title"), help_text=_(""))
    lod = forms.ChoiceField(label=_("Level of Description"),
                    required=False, choices=terms.LEVELS_OF_DETAIL)
    access_conditions = FreeTextField(label=_("Access Conditions"), 
					required=False, help_text=_("TODO: Help text"))
    accruals = FreeTextField(label=_("Accruals"), 
					required=False, help_text=_("TODO: Help text"))
    acquisition = FreeTextField(label=_("Immediate source of acquisition or transfer"), 
					required=False, help_text=_("TODO: Help text"))
    alternate_title = FreeTextField(label=_("Alternate Title"), 
					required=False, help_text=_("TODO: Help text"))
    appraisal = FreeTextField(label=_("Appraisal"), 
					required=False, help_text=_("TODO: Help text"))
    archival_history = FreeTextField(label=_("Archival History"), 
					required=False, help_text=_("TODO: Help text"))
    arrangement = FreeTextField(label=_("Arrangement"), 
					required=False, help_text=_("TODO: Help text"))
    edition = FreeTextField(label=_("Edition"), 
					required=False, help_text=_("TODO: Help text"))
    extent_and_medium = FreeTextField(label=_("Extent and Medium"), 
					required=False, help_text=_("TODO: Help text"))
    finding_aids = FreeTextField(label=_("Finding Aids"), 
					required=False, help_text=_("TODO: Help text"))
    institution_responsible_identifier = FreeTextField(label=_("Institution Responsible Identifier"), 
					required=False, help_text=_("TODO: Help text"))
    location_of_copies = FreeTextField(label=_("Location of Copies"), 
					required=False, help_text=_("TODO: Help text"))
    location_of_originals = FreeTextField(label=_("Location of Originals"), 
					required=False, help_text=_("TODO: Help text"))
    notes = FreeTextField(label=_("Notes"), 
					required=False, help_text=_("TODO: Help text"))
    physical_characteristics = FreeTextField(label=_("Physical Characteristics"), 
					required=False, help_text=_("TODO: Help text"))
    related_units_of_description = FreeTextField(label=_("Related Units of Description"), 
					required=False, help_text=_("TODO: Help text"))
    reproduction_conditions = FreeTextField(label=_("Reproduction Conditions"), 
					required=False, help_text=_("TODO: Help text"))
    revision_history = FreeTextField(label=_("Revision History"), 
					required=False, help_text=_("TODO: Help text"))
    rules = FreeTextField(label=_("Rules"), 
					required=False, help_text=_("TODO: Help text"))
    scope_and_content = FreeTextField(label=_("Scope and Content"), 
					required=False, help_text=_("TODO: Help text"))
    sources = FreeTextField(label=_("Sources"), 
					required=False, help_text=_("TODO: Help text"))
    #languages = forms.MultipleChoiceField(label=_("Language of Materials"), 
    #                choices=utils.language_choices(), required=False, help_text=_("TODO: Help text"))
    #languages_of_description = forms.MultipleChoiceField(label=_("Language of Description"),
    #                choices=utils.language_choices(), required=False, help_text=_("TODO: Help text"))
    #scripts = forms.MultipleChoiceField(label=_("Script of Materials"),
    #                choices=utils.script_choices(), required=False, help_text=_("TODO: Help text"))
    #scripts_of_description = forms.MultipleChoiceField(label=_("Script of Description"),
    #                choices=utils.script_choices(), required=False, help_text=_("TODO: Help text"))


class RepositoryEditForm(PortalEntityForm):
    languages = LanguageSelectFormField()
    scripts = ScriptSelectFormField()
    class Meta:
        model = models.Repository


class AuthorityEditForm(PortalEntityForm):
    languages = LanguageSelectFormField()
    scripts = ScriptSelectFormField()
    class Meta:
        model = models.Authority

class RestoreRevisionForm(forms.Form):
    """Restore a revision of an object."""

def propertyformset_factory(topclass, propname):
    propcls = models.propertyproxy_factory(propname)
    return inlineformset_factory(
            topclass, propcls, fields=("value",), extra=1)


# FIXME: !!! The OtherName formsets below are created using the Collection
# as the primary model, but they're also used in the repository and
# authority forms. This doesn't seem to matter, because when they're
# constructed the primary model seems to be overridden by the instance 
# argument given, but it's obviously still wrong and bug-prone.
# The alternative is lots of ugly duplication or another exceedingly
# meta 'factory' function, neither of which are nice options.

DateFormSet = inlineformset_factory(models.Collection, models.FuzzyDate,
        form=FuzzyDateForm, extra=1)


OtherNameFormSet = inlineformset_factory(models.Collection, models.OtherFormOfName,
        form=OtherNameForm, extra=1)


ParallelNameFormSet = inlineformset_factory(models.Collection, models.ParallelFormOfName,
        form=OtherNameForm, extra=1)


ContactFormSet = inlineformset_factory(models.Repository, models.Contact,
        form=ContactForm, extra=1)


