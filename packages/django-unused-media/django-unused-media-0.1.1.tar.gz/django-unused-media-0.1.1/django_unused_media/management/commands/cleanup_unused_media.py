# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.management.base import BaseCommand

from django_unused_media.cleanup import get_unused_media

import os


class Command(BaseCommand):

    help = "Clean unused media files which have no reference in models"

    def add_arguments(self, parser):

        parser.add_argument('--noinput',
                            dest='interactive',
                            action='store_true',
                            default=True,
                            help='Do not ask confirmation')

    def handle(self, *args, **options):

        unused_media = get_unused_media()

        if options.get('interactive'):

            self.stdout.write('These files will be deleted:')

            for f in unused_media:
                self.stdout.write(f)

            try: input = raw_input
            except NameError: pass

            if input('Are you sure you want to remove %s unused files? (Y/n)' % len(unused_media)) != 'Y':
                self.stdout.write('Interrupted by user. Exit.')
                return

        for f in unused_media:
            self.stdout.write('Remove %s' % f)
            os.remove(os.path.join(settings.MEDIA_ROOT, f))

        self.stdout.write('Done. %s unused files have been removed' % len(unused_media))
