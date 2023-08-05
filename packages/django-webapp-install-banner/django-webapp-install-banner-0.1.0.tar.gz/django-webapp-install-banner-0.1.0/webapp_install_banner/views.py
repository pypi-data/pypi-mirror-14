from django.http import JsonResponse
from django.templatetags.static import static
from . import settings


def manifest(request):
    manifest = settings.MANIFEST.copy()

    if "name" not in manifest:
        manifest["name"] = manifest["short_name"]

    manifest["short_name"] = unicode(manifest["short_name"])
    manifest["name"] = unicode(manifest["name"])

    manifest["start_url"] = unicode(manifest["start_url"])
    args = "?" + settings.WEBAPP_FIELD + "=1"
    manifest["start_url"] = manifest["start_url"] + args

    for icon in manifest["icons"]:
        icon["src"] = static(icon["src"])

    return JsonResponse(manifest)
