# -*- coding: utf-8 -*-
import ast
from django.db import models
from django.conf import settings

from pyzotero import zotero

library_id = settings.Z_ID
library_type = settings.Z_LIBRARY_TYPE
api_key = settings.Z_API_KEY
try:
    NN = settings.Z_NN
except AttributeError:
    NN = 'N.N.'


def fetch_bibtex(zot_key):
    """ fetches the bibtex dict of the passed in key """
    result = {}
    zot = zotero.Zotero(library_id, library_type, api_key)
    try:
        result['bibtex'] = zot.item(zot_key, format='bibtex').entries_dict
        result['error'] = None
    except Exception as e:
        result['bibtex'] = None
        result['error'] = "{}".format(e)

    return result


class ZotItem(models.Model):

    """ Stores main bibliographic information of a Zotero Item """

    zot_key = models.CharField(
        max_length=20, primary_key=True, verbose_name='key',
        help_text="The Zotero Item Key"
    )
    zot_creator = models.TextField(
        blank=True, verbose_name="creators",
        help_text="Stores all information from Zotero's 'creators' field."
    )
    zot_date = models.TextField(
        blank=True, verbose_name="date",
        help_text="Stores all information from Zotero's 'date' field."
    )
    zot_item_type = models.TextField(
        blank=True, verbose_name="itemType",
        help_text="Stores all information from Zotero's 'itemType' field."
    )
    zot_title = models.TextField(
        blank=True, verbose_name="title",
        help_text="Stores all information from Zotero's 'title' field."
    )
    zot_pub_title = models.TextField(
        blank=True, verbose_name="publicationTitle",
        help_text="Stores all information from zoteros 'publicationTitle' field."
    )
    journal_abbreviation = models.TextField(
        blank=True, null=True, verbose_name="journal abbreviation",
        help_text="Stores all information from Zotero's 'journalAbbreviation' field."
    )
    short_title = models.TextField(
        blank=True, null=True, verbose_name="short title",
        help_text="Stores all information from Zotero's 'shortTitle' field."
    )
    proceedings_title = models.TextField(
        blank=True, null=True, verbose_name="proceedings title",
        help_text="Stores all information from Zotero's 'proceedingsTitle' field."
    )
    conference_name = models.TextField(
        blank=True, null=True, verbose_name="conference name",
        help_text="Stores all information from Zotero's 'conferenceName' field."
    )
    abstract_note = models.TextField(
        blank=True, null=True, verbose_name="abstract note",
        help_text="Stores all information from Zotero's 'abstractNote' field."
    )
    series = models.TextField(
        blank=True, null=True, verbose_name="series",
        help_text="Stores all information from Zotero's 'series' field."
    )
    series_number = models.TextField(
        blank=True, null=True, verbose_name="series number",
        help_text="Stores all information from Zotero's 'seriesNumber' field."
    )
    volume = models.TextField(
        blank=True, null=True, verbose_name="volume",
        help_text="Stores all information from Zotero's 'volume' field."
    )
    number_of_volumes = models.TextField(
        blank=True, null=True, verbose_name="number of volumes",
        help_text="Stores all information from Zotero's 'numberOfVolumes' field."
    )
    issue = models.TextField(
        blank=True, null=True, verbose_name="issue",
        help_text="Stores all information from Zotero's 'issue' field."
    )
    edition = models.TextField(
        blank=True, null=True, verbose_name="edition",
        help_text="Stores all information from Zotero's 'edition' field."
    )
    place = models.TextField(
        blank=True, null=True, verbose_name="place",
        help_text="Stores all information from Zotero's 'place' field."
    )
    publisher = models.TextField(
        blank=True, null=True, verbose_name="publisher",
        help_text="Stores all information from Zotero's 'publisher' field."
    )
    language = models.TextField(
        blank=True, null=True, verbose_name="language",
        help_text="Stores all information from Zotero's 'language' field."
    )
    isbn = models.TextField(
        blank=True, null=True, verbose_name="isbn",
        help_text="Stores all information from Zotero's 'ISBN' field."
    )
    issn = models.TextField(
        blank=True, null=True, verbose_name="issn",
        help_text="Stores all information from Zotero's 'ISSN' field."
    )
    doi = models.TextField(
        blank=True, null=True, verbose_name="doi",
        help_text="Stores all information from Zotero's 'DOI' field."
    )
    url = models.TextField(
        blank=True, null=True, verbose_name="url",
        help_text="Stores all information from Zotero's 'url' field."
    )
    access_date = models.TextField(
        blank=True, null=True, verbose_name="access date",
        help_text="Stores all information from Zotero's 'accessDate' field."
    )
    archive = models.TextField(
        blank=True, null=True, verbose_name="archive",
        help_text="Stores all information from Zotero's 'archive' field."
    )
    archive_location = models.TextField(
        blank=True, null=True, verbose_name="archive location",
        help_text="Stores all information from Zotero's 'archiveLocation' field."
    )
    library_catalog = models.TextField(
        blank=True, null=True, verbose_name="library catalog",
        help_text="Stores all information from Zotero's 'libraryCatalog' field."
    )
    call_number = models.TextField(
        blank=True, null=True, verbose_name="call number",
        help_text="Stores all information from Zotero's 'callNumber' field."
    )
    rights = models.TextField(
        blank=True, null=True, verbose_name="rights",
        help_text="Stores all information from Zotero's 'rights' field."
    )
    extra = models.TextField(
        blank=True, null=True, verbose_name="extra",
        help_text="Stores all information from Zotero's 'extra' field."
    )
    # tags and collections are arrays, like creator, not using ArrayField to keep sqllite compatability
    tags = models.TextField(
        blank=True, null=True, verbose_name="tag",
        help_text="Stores all information from Zotero's 'tags' field."
    )
    collections= models.TextField(
        blank=True, null=True, verbose_name="collection",
        help_text="Stores all information from Zotero's 'collections' field."
    )
    date_added = models.DateTimeField(
        blank=True, null=True, verbose_name="dateAdded",
        help_text="Stores all information from Zotero's 'dateAdded' field."
    )
    date_modified = models.DateTimeField(
        blank=True, null=True, verbose_name="dateModified",
        help_text="Stores all information from Zotero's 'dateModified' field."
    )
    zot_pages = models.TextField(
        blank=True, verbose_name="pages",
        help_text="Stores all information from Zotero's 'numPages' field."
    )
    zot_version = models.IntegerField(
        blank=True, null=True, verbose_name="version",
        help_text="Stores all information from Zotero's 'version' field."
    )
    zot_html_link = models.CharField(
        blank=True, verbose_name="selflink html", max_length=500,
        help_text="Stores all information from Zotero's 'selflink' field."
    )
    zot_api_link = models.CharField(
        blank=True, verbose_name="selflink api", max_length=500,
        help_text="Stores all information from Zotero's self api link field."
    )
    zot_bibtex = models.TextField(
        blank=True, verbose_name="bibtex",
        help_text="Stores the item's bibtex representation."
    )

    class Meta:
        ordering = ['-zot_version']

    def __str__(self):
        if self.zot_bibtex:
            return "{}".format(self.zot_bibtex)
        else:
            repr = ""
            if self.author:
                repr += "{}".format(self.author)
            if self.zot_title:
                repr += ": {}".format(self.zot_title)
            if self.zot_pub_title:
                repr += "; {}".format(self.zot_pub_title)
            if self.zot_date:
                repr += " ({})".format(self.zot_date)
            return repr

    def save(self, get_bibtex=False, *args, **kwargs):
        if get_bibtex:
            bibtex = fetch_bibtex(self.zot_key)
            if bibtex['bibtex']:
                self.zot_bibtex = "{}".format(bibtex['bibtex'])
                self.save()
            else:
                pass
            super(ZotItem, self).save(*args, **kwargs)
        else:
            super(ZotItem, self).save(*args, **kwargs)

    @property
    def author(self):
        authors = []
        author_list = ast.literal_eval(self.zot_creator)
        for x in author_list:
            try:
                author = f"{x['firstName']} {x['lastName']}"
            except KeyError:
                author = f"{x.get('name', '')}"
            authors.append(author.strip())
        author_name = " / ".join(authors)
        if author_name:
            return author_name
        else:
            return NN
