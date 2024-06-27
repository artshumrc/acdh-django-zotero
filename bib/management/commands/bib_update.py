import os
import datetime
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.core.management.base import BaseCommand, CommandError, CommandParser
from bib.zot_utils import items_to_dict, create_zotitem
from bib.models import ZotItem

library_id = settings.Z_ID
library_type = settings.Z_LIBRARY_TYPE
api_key = settings.Z_API_KEY

class Command(BaseCommand):

    """ Imports items from zotero-bib """

    help = "Imports all items from zotero-bib"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--limit',
            dest='limit',
            help="Max number of items to import"
        )
        parser.add_argument(
            '--since',
            dest='since',
            help="The version (string) from which on items should be imported"
        )
        parser.add_argument(
            '--citation_format',
            dest='citation_format',
            help="The format in which the citation should be returned"
        )
        parser.add_argument(
            '--get_bibtext',
            dest='get_bibtext',
            help="If the bibtex should be fetched"
        ),
        parser.add_argument(
            '--get_citation',
            dest='get_citation',
            help="If the citation should be fetched"
        )

    def handle(self, *args, **options):
        citation_format = options['citation_format'] if options['citation_format'] else getattr(settings, 'Z_CITATION_FORMAT', None)
        get_bibtext = options['get_bibtext'] if options['get_bibtext'] else False
        get_citation = options['get_citation'] if options['get_citation'] else False
        first_object = ZotItem.objects.all()[:1].get()
        limit = int(options['limit']) if options['limit'] else None
        since = options['since'] if options['since'] else first_object.zot_version

        self.stdout.write(
            self.style.SUCCESS("{}, {}".format(first_object, since))
        )

        self.stdout.write(
            self.style.SUCCESS("{}, {}".format(limit, since))
        )
        self.stdout.write(
            self.style.SUCCESS("started: {}".format(datetime.datetime.now()))
        )
        items = items_to_dict(library_id, library_type, api_key, limit=limit, since_version=since, citation_format=citation_format)
        self.stdout.write(
            self.style.SUCCESS("fetched {} items".format(len(items['items'])))
        )
        self.stdout.write(
            self.style.SUCCESS("{}".format(datetime.datetime.now()))
        )
        self.stdout.write(
            self.style.SUCCESS('starting creating/updating models now')
        )
        for x in items['bibs']:
            temp_item = create_zotitem(x, get_bibtext=get_bibtext, get_citation=get_citation)
            self.stdout.write(
                self.style.SUCCESS('created: {}'.format(temp_item))
            )
        self.stdout.write(
            self.style.SUCCESS("ended: {}".format(datetime.datetime.now()))
        )
