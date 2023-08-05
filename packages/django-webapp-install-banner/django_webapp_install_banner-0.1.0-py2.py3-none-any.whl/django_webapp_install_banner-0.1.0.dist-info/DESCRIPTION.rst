=============================
django-webapp-install-banner
=============================

.. image:: https://badge.fury.io/py/django-webapp-install-banner.png
    :target: https://badge.fury.io/py/django-webapp-install-banner

.. image:: https://travis-ci.org/ferranp/django-webapp-install-banner.png?branch=master
    :target: https://travis-ci.org/ferranp/django-webapp-install-banner

Add web App install banner to django project"

Documentation
-------------

The full documentation is at https://django-webapp-install-banner.readthedocs.org.

Quickstart
----------

Install django-webapp-install-banner::

    pip install django-webapp-install-banner

Add to your django settings.py file::

    INSTALLED_APPS += ('webapp_install_banner',)
    MIDDLEWARE_CLASSES += ('webapp_install_banner.middleware.WebAppMiddleware',)

    MANIFEST = {
        "short_name": _("Project name"),
        "name": _("Project log name"),
        "icons": [
            {
                "src": "img/favicon-96x96.png",
                "sizes": "96x96",
                "type": "image/png"
            },
            {
                "src": "img/apple-touch-icon-144x144.png",
                "sizes": "144x144",
                "type": "image/png"
            },
            {
                "src": "img/android-chrome-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            }
        ],
        "start_url": reverse_lazy("index"),
        "display": "standalone"
    }

Add to your urls.py::

    urlpatterns += (url(r'', include('webapp_install_banner.urls')),)

Add to your base template html header::

    {% load webapp_tags %}
    {% webapp_manifest %}


Features
--------

Adds a manifest.json file, and manages detecting if started from webapp.

TODO: Add service worker file.

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage




History
-------

0.1.0 (2016-03-27)
++++++++++++++++++

* First release on PyPI.

