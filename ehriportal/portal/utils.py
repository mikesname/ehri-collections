"""Utility functions for dealing with repository and geo data."""

from incf.countryutils import transformations
import babel

# Hacky dictionary of official country/languages names
# we want to substitute for friendlier versions... 
# A more permenant solution is needed to this.
SUBNAMES = {
    "United Kingdom of Great Britain & Northern Ireland": "United Kingdom",
}

def language_name_from_code(code, locale="en"):
    """Get lang display name."""
    # TODO: Find the correct way to do this
    return babel.Locale(locale).languages.get(code, "")


def get_country_from_code(code):
    """Get the country code from a coutry name."""
    try:
        name = transformations.cc_to_cn(code)
        return SUBNAMES.get(name, name)
    except KeyError:
        pass


