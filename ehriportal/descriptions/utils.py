"""Utils for working with collection descriptions."""

import babel

def language_name_from_code(code):
    """Get lang display name."""
    # TODO: Find the correct way to do this
    return babel.Locale("en").languages.get(code, "")
