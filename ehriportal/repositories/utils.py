"""Utility functions for dealing with repository and geo data."""

from incf.countryutils import data as countrydata

def get_country_from_code(code):
    """Get the country code from a coutry name."""
    ccn = countrydata.cca2_to_ccn.get(code)
    if ccn is None:
        return
    return countrydata.ccn_to_cn.get(ccn)


