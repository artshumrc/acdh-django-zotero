from pyzotero import zotero
from django.conf import settings
from bib.models import ZotItem


def items_to_dict(library_id, library_type, api_key, limit=15, since_version=None, citation_format=None):

    """
    returns a dict with keys 'error' containing possible error-msgs,
    'items' a list of fetched zotero items and
    'bibs' a list of dicts ready for creating ZotItem objects
    """

    zot = zotero.Zotero(library_id, library_type, api_key)
    result = {}
    error = None
    items = None
    bibs = []
    if since_version:
        try:
            items = zot.everything(zot.top(since=since_version))
            bibtexs = zot.everything(zot.top(format='bibtex', since=since_version))
        except Exception as e:
            error = "{}".format(e)
            items = None
            bibtexs = None
    elif limit:
        try:
            items = zot.top(limit=limit)
            bibtexs = zot.everything(zot.top(format='bibtex', limit=limit))
        except Exception as e:
            error = "{}".format(e)
            items = None
            bibtexs = None
    else:
        try:
            items = zot.everything(zot.top())
            bibtexs = zot.everything(zot.top(format='bibtex'))
        except Exception as e:
            error = "{}".format(e)
            items = None
            bibtexs = None

    result['items'] = items
    result['error'] = error
    result['bibtexs'] = bibtexs

    if items:
        bibs = []
        c = 0
        for x in items:
            bib = {}
            bib['key'] = "{}".format(x['data'].get('key'))
            bib['creators'] = "{}".format(x['data'].get('creators'))
            bib['date'] = "{}".format(x['data'].get('date'))
            bib['itemType'] = "{}".format(x['data'].get('itemType'))
            bib['title'] = "{}".format(x['data'].get('title'))
            bib['shortTitle'] = "{}".format(x['data'].get('shortTitle'))
            bib['publicationTitle'] = "{}".format(x['data'].get('publicationTitle'))
            bib['journalAbbreviation'] = "{}".format(x['data'].get('journalAbbreviation'))
            bib['proceedingsTitle'] = "{}".format(x['data'].get('proceedingsTitle'))
            bib['conferenceName'] = "{}".format(x['data'].get('conferenceName'))
            bib['abstractNote'] = "{}".format(x['data'].get('abstractNote'))
            bib['series'] = "{}".format(x['data'].get('series'))
            bib['seriesNumber'] = "{}".format(x['data'].get('seriesNumber'))
            bib['volume'] = "{}".format(x['data'].get('volume'))
            bib['numberOfVolumes'] = "{}".format(x['data'].get('numberOfVolumes'))
            bib['issue'] = "{}".format(x['data'].get('issue'))
            bib['edition'] = "{}".format(x['data'].get('edition'))
            bib['place'] = "{}".format(x['data'].get('place'))
            bib['publisher'] = "{}".format(x['data'].get('publisher'))
            bib['language'] = "{}".format(x['data'].get('language'))
            bib['isbn'] = "{}".format(x['data'].get('ISBN'))
            bib['issn'] = "{}".format(x['data'].get('ISSN'))
            bib['doi'] = "{}".format(x['data'].get('DOI'))
            bib['url'] = "{}".format(x['data'].get('url'))
            bib['accessDate'] = "{}".format(x['data'].get('accessDate'))
            bib['archive'] = "{}".format(x['data'].get('archive'))
            bib['archiveLocation'] = "{}".format(x['data'].get('archiveLocation'))
            bib['libraryCatalog'] = "{}".format(x['data'].get('libraryCatalog'))
            bib['callNumber'] = "{}".format(x['data'].get('callNumber'))
            bib['rights'] = "{}".format(x['data'].get('rights'))
            bib['extra'] = "{}".format(x['data'].get('extra'))
            bib['tags'] = "{}".format(x['data'].get('tags'))
            bib['collections'] = "{}".format(x['data'].get('collections'))
            bib['dateAdded'] = "{}".format(x['data'].get('dateAdded'))
            bib['dateModified'] = "{}".format(x['data'].get('dateModified'))
            bib['pages'] = "{}".format(x['data'].get('numPages'))
            bib['version'] = "{}".format(x['data'].get('version'))
            bib['zot_html_link'] = "{}".format(x['links']['alternate']['href'])
            bib['zot_api_link'] = "{}".format(x['links']['self']['href'])
            if len(bibtexs.entries) == len(items):
                try:
                    bib['zot_bibtex'] = "{}".format(bibtexs.entries[c])
                except IndexError:
                    bib['zot_bibtex'] = ""
            else:
                bib['zot_bibtex'] = ""
            if citation_format:
                try:
                    citation = zot.top(
                        format="json",
                        itemKey=x['data'].get('key'),
                        content="bib",
                        style=citation_format
                    )
                    bib['citation'] = citation
                except Exception as e:
                    bib['citation'] = ""
            else:
                bib['citation'] = ""
            bibs.append(bib)
            c += 1

    result['bibs'] = bibs
    return result


def create_zotitem(bib_item, get_bibtex=False, get_citation=False):
    """
    takes a dict with bib info created by 'items_to_dict'
    and creates/updates a ZotItem object
    """
    x = bib_item
    temp_item, _ = ZotItem.objects.get_or_create(
        zot_key=x['key']
    )
    temp_item.zot_creator = x['creators']
    temp_item.zot_date = x['date']
    temp_item.zot_item_type = x['itemType']
    temp_item.zot_title = x['title']
    temp_item.zot_pub_title = x['publicationTitle']
    temp_item.journal_abbreviation = x['journalAbbreviation']
    temp_item.short_title = x['shortTitle']
    temp_item.proceedings_title = x['proceedingsTitle']
    temp_item.conference_name = x['conferenceName']
    temp_item.abstract_note = x['abstractNote']
    temp_item.series = x['series']
    temp_item.series_number = x['seriesNumber']
    temp_item.volume = x['volume']
    temp_item.number_of_volumes = x['numberOfVolumes']
    temp_item.issue = x['issue']
    temp_item.edition = x['edition']
    temp_item.place = x['place']
    temp_item.publisher = x['publisher']
    temp_item.language = x['language']
    temp_item.isbn = x['isbn']
    temp_item.issn = x['issn']
    temp_item.doi = x['doi']
    temp_item.url = x['url']
    temp_item.access_date = x['accessDate']
    temp_item.archive = x['archive']
    temp_item.archive_location = x['archiveLocation']
    temp_item.library_catalog = x['libraryCatalog']
    temp_item.call_number = x['callNumber']
    temp_item.rights = x['rights']
    temp_item.extra = x['extra']
    temp_item.tags = x['tags']
    temp_item.collections = x['collections']
    temp_item.date_added = x['dateAdded']
    temp_item.date_modified = x['dateModified']
    temp_item.zot_pages = x['pages']
    temp_item.zot_version = x['version']
    temp_item.zot_html_link = x['zot_html_link']
    temp_item.zot_api_link = x['zot_api_link']
    temp_item.citation = x['citation']
    # why is bibtex updated both here and in the model.save()?
    # create_zotitem(get_bibtext=True) is never called in the management commands
    # Following this pattern for citation for now.
    try:
        temp_item.zot_bibtex = x['zot_bibtex']
    except KeyError:
        pass
    temp_item.save(get_bibtex=get_bibtex, get_citation=get_citation)
    return temp_item