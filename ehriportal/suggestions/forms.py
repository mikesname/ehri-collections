"""Form for submitting suggestions."""

from django import forms

from suggestions import models

class SuggestionForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Name",
            widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(label="Email", required=False,
            widget=forms.TextInput(attrs={'placeholder': 'Email (Optional)'}))
    types = forms.ModelMultipleChoiceField(
                required=False,
                queryset=models.SuggestionType.objects.all().order_by("name"))
    text = forms.CharField(widget=forms.Textarea(
                attrs={'rows':5, 'placeholder': "Comments"}))

    class Meta:
        model = models.Suggestion
        fields = ("name", "email", "types", "text",)
