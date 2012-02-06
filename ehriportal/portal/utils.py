"""Utility functions for dealing with repository and geo data."""

from incf.countryutils import transformations
import babel

def language_name_from_code(code, locale="en"):
    """Get lang display name."""
    # TODO: Find the correct way to do this
    return babel.Locale(locale).languages.get(code, "")


def get_country_from_code(code):
    """Get the country code from a coutry name."""
    try:
        return transformations.cc_to_cn(code)
    except KeyError:
        pass


