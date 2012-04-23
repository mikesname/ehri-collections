from django import template

from reversion.helpers import generate_patch_html
import reversion

register = template.Library()


#class DiffNode(template.Node):
#    def __init__(self, v1, v2, field):
#        self.v1 = template.Variable(v1)
#        self.v2 = template.Variable(v2)
#        self.field = field
#
#def reversion_diff(parser, token):
#    msg = "%r tag requires version 1, version 2, and field arguments" % token.contents.split()[0]
#    try:
#        tag_name, v1, v2, field = token.split_contents()
#    except ValueError:
#        raise template.TemplateSyntaxError(msg)
#    if not isinstance(v1, reversion.models.Version) and \
#            isinstance(v2, reversion.models.Version):
#        raise template.TemplateSyntaxError(msg)
#    return DiffNode(v1, v2, field)


@register.simple_tag(name="vdiff")
def version_diff(v1, v2, field):
    return generate_patch_html(v1, v2, field)

