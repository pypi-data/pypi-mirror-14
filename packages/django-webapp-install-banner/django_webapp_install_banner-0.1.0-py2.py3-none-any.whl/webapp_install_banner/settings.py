import os
from django.conf import settings


WEBAPP_FIELD = getattr(settings, "WEBAPP_FIELD", "from_web_app")
WEBAPP_COOKIE = getattr(settings, "WEBAPP_COOKIE", "from_web_app")

BASE_MANIFEST = {
    "short_name": os.path.basename(settings.BASE_DIR),
    "icons": [],
    "start_url": "./",
    "display": "standalone"
}

MANIFEST = BASE_MANIFEST.copy()
MANIFEST.update(getattr(settings, "MANIFEST", {}))
