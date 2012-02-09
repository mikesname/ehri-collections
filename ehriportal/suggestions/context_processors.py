"""Add the form to every request's context, pre-populated by
some useful information."""

from suggestions import forms

def suggestions_form(request):
    initial = {}
    if request.user.is_authenticated():
        name = request.user.get_full_name()
        try:
            name = request.user.profile_set.all()[0].name
        except IndexError:
            pass
        initial["name"] = name or request.user.username
        initial["email"]  = request.user.email
    form = forms.SuggestionForm(initial=initial, prefix="suggestion")
    return dict(suggestionform=form)

