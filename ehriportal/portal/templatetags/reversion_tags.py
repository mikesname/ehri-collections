from django import template

from reversion.helpers import generate_patch_html
import reversion

register = template.Library()


@register.simple_tag(name="vdiff")
def version_diff(v1, v2, field):
    """Return HTML showing the differences between two fields."""
    return generate_patch_html(v1, v2, field, cleanup="semantic")

