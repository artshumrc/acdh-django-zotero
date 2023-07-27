# -*- coding: utf-8 -*-
from django.urls import re_path
from . import views
from . import dal_views

app_name = 'bib'

urlpatterns = [
    re_path(r'^synczotero/$', views.sync_zotero, name="synczotero"),
    re_path(r'^synczotero/update$', views.update_zotitems, name="synczotero_update"),
    re_path(
        r'^zotitem-autocomplete/$', dal_views.ZotItemAC.as_view(),
        name='zotitem-autocomplete',
    ),
]
