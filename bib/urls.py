# -*- coding: utf-8 -*-
from django.urls import path
from . import views
from . import dal_views

app_name = 'bib'

urlpatterns = [
    path('synczotero/', views.sync_zotero, name="synczotero"),
    path('synczotero/update/', views.update_zotitems, name="synczotero_update"),
    path(
        'zotitem-autocomplete/',
        dal_views.ZotItemAC.as_view(),
        name='zotitem-autocomplete',
    ),
]
