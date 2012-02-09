"""Form for submitting suggestions."""

from django import forms
from django.utils.translation import ugettext as _

from suggestions import models

class SuggestionForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label=_("Name"),
            widget=forms.TextInput(attrs={'placeholder': _('Name')}))
    email = forms.EmailField(label=_("Email"), required=False,
            widget=forms.TextInput(attrs={'placeholder': _('Email (Optional)')}))
    meta = forms.CharField(widget=forms.HiddenInput())
    text = forms.CharField(widget=forms.Textarea(
                attrs={'rows':5, 'placeholder': _("Let us know what you think...")}))

    class Meta:
        model = models.Suggestion
        fields = ("name", "email", "text",)
