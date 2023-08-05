from django import template
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from .. import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def webapp_manifest(context):
    request = context['request']

    if settings.WEBAPP_COOKIE in request.COOKIES:
        return ""

    if settings.WEBAPP_FIELD in request.GET:
        return ""

    webapp_path = unicode(settings.MANIFEST['start_url'])

    if request.path != webapp_path:
        return ""

    url = reverse("webapp_manifest")
    return mark_safe('<link rel="manifest" href="%s">' % url)
