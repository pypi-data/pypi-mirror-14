from django.conf.urls import url

import views

urlpatterns = (
    url(r'^manifest.json$', views.manifest, name='webapp_manifest'),
)
