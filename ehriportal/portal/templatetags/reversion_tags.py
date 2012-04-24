from django import template

from reversion.helpers import generate_patch_html
import reversion

register = template.Library()



@register.simple_tag(name="vdiff")
def version_diff(v1, v2, field):
    """Return HTML showing the differences between two fields."""
    return generate_patch_html(v1, v2, field, cleanup="semantic")

@register.simple_tag(name="list_test")
def list_test():
    return ["one", "two", "three"]

@register.simple_tag(name="object_vdiff")
def set_version_diff(obj, v1, v2, setname, field):
    """Lookup an object that isn't the primary one, but is part
    of the same revision set, i.e. a foreign-key related date.
    TODO: Find a better way of doing this - it is probably 
    HORRIBLY slow (although only used on the diff page, so not
    that important."""
    import reversion
    from django.contrib.contenttypes.models import ContentTypeManager
    from diff_match_patch import diff_match_patch
    dmp = diff_match_patch()
    # FIXME: As well as being gross, this is fragile because
    # it doesn't account for more than one 
    model = getattr(obj, setname).model
    ctype = ContentTypeManager().get_for_model(model)
    if not model in reversion.get_registered_models():
        raise AttributeError("Model %r is not registered as a reversion model.")
    set1 = v1.revision.version_set.filter(content_type=ctype)
    set2 = v2.revision.version_set.filter(content_type=ctype)
    setobj1 = model.objects.filter([v.object_id for v in set1])
    setobj2 = model.objects.filter([v.object_id for v in set2])
    setids1 = [v.object_id for v in set1]
    setids2 = [v.object_id for v in set2]
    added = []
    persisted = []
    deleted = []
    # NB: This assumes that if a version's object
    # is 'None' than it's not in a previous version.
    for vers in set1:
        if vers.object:
            if vers.object_id not in setids2:
                added.append(vers.object)
            else:
                persisted.append(vers.object)
    for vers in set2:
        if vers.object_id not in setids1:
            deleted.append(vers)
    out = []
    for vers in added:
        diffs = dmp.diff_main(unicode(vers.field_dict[field]), u"")
        dmp.diff_cleanupSemantic(diffs)
        out.append(dmp.diff_prettyHtml(diffs))
    for vers in persisted:
        out.append(vers.field_dict[field])
    for vers in deleted:
        diffs = dmp.diff_main(u"", unicode(vers.field_dict[field]))
        dmp.diff_cleanupSemantic(diffs)
        out.append(dmp.diff_prettyHtml(diffs))
    return u"<li>" + out.join(u"</li><li>") + u"</li>"











