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
    name = forms.CharField(label=_("Name"), help_text=_("TODO: Help text"))
    level_of_detail = forms.ChoiceField(label=_("Level of Description"),
                    required=False, choices=terms.LEVELS_OF_DETAIL)
    publication_status = forms.ChoiceField(label=_("Publication Status"), 
                choices=terms.PUBLICATION_STATUS, help_text=_("Status of this item with regards to "
                                                            "public visibility."))
    revision_comment = forms.CharField(required=False, widget=forms.TextInput(attrs={
                "placeholder": _("Summary of changes (optional)"),
            }))

class FreeTextField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(FreeTextField, self).__init__(*args, **kwargs)
        self.widget = forms.Textarea()

class ContactForm(forms.Form):
    """Form representing a repository's contact information."""
    primary = forms.BooleanField(_("Primary Contact"))
    contact_person = forms.CharField(label=_("Contact Person"), max_length=255, required=False)
    street_address = FreeTextField(label=_("Street Address"), required=False)
    city = forms.CharField(label=_("City"), max_length=100, required=False)
    region = forms.CharField(label=_("Region"), max_length=100, required=False)
    postal_code = forms.CharField(label=_("Postal Code"), max_length=100, required=False)
    country_code = forms.ChoiceField(label=_("Country"), required=False,
            choices=[(None, "------")] + list(utils.country_choices()))
    website = forms.URLField(label=_("Website"), required=False)
    email = forms.EmailField(label=_("Email"), required=False)
    telephone = forms.CharField(label=_("Telephone"), max_length=100, required=False)
    fax = forms.CharField(label=_("Fax"), max_length=100, required=False)
    contact_type = forms.CharField(label=_("Contact Type"),
            max_length=100, required=False)
    note = FreeTextField(label=_("Notes"), required=False)


class CollectionEditForm(PortalEntityForm):
    """Form representing an ISAD(G) collection entry (minus its relations
    to other entities such as the repository and creator.)"""
    identifier = forms.CharField(label=_("Identifier"), help_text=_(""))
    name = forms.CharField(label=_("Title"), help_text=_(""))
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
    """Form details for an ISDIAH repository."""
    identifier = forms.CharField(label=_("Identifier"), help_text=_(""))
    name = forms.CharField(label=_("Title"), help_text=_(""))
    type_of_entity = forms.ChoiceField(label=_("Type of Entity"),
                choices=terms.ENTITY_TYPES)
    access_conditions = FreeTextField(label=_("Access Conditions"),
					required=False, help_text=_("TODO: Help text"))
    buildings = FreeTextField(label=_("Buildings"),
					required=False, help_text=_("TODO: Help text"))
    collecting_policies = FreeTextField(label=_("Collecting Policies"),
					required=False, help_text=_("TODO: Help text"))
    dates_of_existence = FreeTextField(label=_("Dates of Existence"),
					required=False, help_text=_("TODO: Help text"))
    disabled_access = FreeTextField(label=_("Disabled Access"),
					required=False, help_text=_("TODO: Help text"))
    finding_aids = FreeTextField(label=_("Finding Aids"),
					required=False, help_text=_("TODO: Help text"))
    functions = FreeTextField(label=_("Functions"),
					required=False, help_text=_("TODO: Help text"))
    general_context = FreeTextField(label=_("General Context"),
					required=False, help_text=_("TODO: Help text"))
    geocultural_context = FreeTextField(label=_("Geocultural Context"),
					required=False, help_text=_("TODO: Help text"))
    history = FreeTextField(label=_("History"),
					required=False, help_text=_("TODO: Help text"))
    holdings = FreeTextField(label=_("Holdings"),
					required=False, help_text=_("TODO: Help text"))
    internal_structures = FreeTextField(label=_("Internal Structures"),
					required=False, help_text=_("TODO: Help text"))
    legal_status = FreeTextField(label=_("Legal Status"),
					required=False, help_text=_("TODO: Help text"))
    maintenance_notes = FreeTextField(label=_("Maintenance Notes"),
					required=False, help_text=_("TODO: Help text"))
    mandates = FreeTextField(label=_("Mandates"),
					required=False, help_text=_("TODO: Help text"))
    opening_times = FreeTextField(label=_("Opening Times"),
					required=False, help_text=_("TODO: Help text"))
    places = FreeTextField(label=_("Places"),
					required=False, help_text=_("TODO: Help text"))
    reproduction_services = FreeTextField(label=_("Reproduction Services"),
					required=False, help_text=_("TODO: Help text"))
    research_services = FreeTextField(label=_("Research Services"),
					required=False, help_text=_("TODO: Help text"))
    rules = FreeTextField(label=_("Rules"),
					required=False, help_text=_("TODO: Help text"))
    sources = FreeTextField(label=_("Sources"),
					required=False, help_text=_("TODO: Help text"))
    #languages = forms.multiplechoicefield(label=_("language of materials"), 
    #                choices=utils.language_choices(), required=false, help_text=_("todo: help text"))
    #scripts = forms.multiplechoicefield(label=_("script of materials"),
    #                choices=utils.script_choices(), required=false, help_text=_("todo: help text"))


class AuthorityEditForm(PortalEntityForm):
    """Form detailing an ISAAR authority file."""
    identifier = forms.CharField(label=_("Identifier"), help_text=_(""))
    name = forms.CharField(label=_("Title"), help_text=_(""))
    type_of_entity = forms.ChoiceField(label=_("Type of Entity"),
                choices=terms.AUTHORITY_TYPES)
    dates_of_existence = FreeTextField(label=_("Dates of Existence"),
					required=False, help_text=_("TODO: Help text"))
    functions = FreeTextField(label=_("Functions"),
					required=False, help_text=_("TODO: Help text"))
    general_context = FreeTextField(label=_("General Context"),
					required=False, help_text=_("TODO: Help text"))
    history = FreeTextField(label=_("History"),
					required=False, help_text=_("TODO: Help text"))
    institution_responsible_identifier = FreeTextField(label=_("Institution Responsible Identifier"),
					required=False, help_text=_("TODO: Help text"))
    internal_structures = FreeTextField(label=_("Internal Structures"),
					required=False, help_text=_("TODO: Help text"))
    legal_status = FreeTextField(label=_("Legal Status"),
					required=False, help_text=_("TODO: Help text"))
    mandates = FreeTextField(label=_("Mandates"),
					required=False, help_text=_("TODO: Help text"))
    places = FreeTextField(label=_("Places"),
					required=False, help_text=_("TODO: Help text"))
    revision_history = FreeTextField(label=_("Revision History"),
					required=False, help_text=_("TODO: Help text"))
    sources = FreeTextField(label=_("Sources"),
					required=False, help_text=_("TODO: Help text"))
    #languages = forms.multiplechoicefield(label=_("language of materials"), 
    #                choices=utils.language_choices(), required=false, help_text=_("todo: help text"))
    #scripts = forms.MultipleChoiceField(label=_("Script of Materials"),
    #                choices=utils.script_choices(), required=False, help_text=_("TODO: Help text"))


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

#DateFormSet = inlineformset_factory(models.Collection, models.FuzzyDate,
#        form=FuzzyDateForm, extra=1)
#
#
#OtherNameFormSet = inlineformset_factory(models.Collection, models.OtherFormOfName,
#        form=OtherNameForm, extra=1)
#
#
#ParallelNameFormSet = inlineformset_factory(models.Collection, models.ParallelFormOfName,
#        form=OtherNameForm, extra=1)
#
#
ContactFormSet = forms.formsets.formset_factory(form=ContactForm, extra=1, can_delete=True)

