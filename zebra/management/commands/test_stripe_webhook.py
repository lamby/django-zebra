import sys

from zebra.signals import WEBHOOK_MAP

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('webhook', metavar='webhook',
            help="Webhook to test")
        parser.add_argument('filenames', nargs='+', metavar='filename',
            help="Filenames to read data from")

    def handle(self, *args, **options):
        for filename in options['filenames']:
            if filename == '-':
                data = sys.stdin.read()
            else:
                with open(filename) as f:
                    data = f.read()

            full_json = json.loads(data)

            signal_name = full_json['type'].replace('.', '_')

            try:
                signal = WEBHOOK_MAP[signal_name]
            except KeyError:
                raise CommandError(
                    "'%s' is not a valid signal name" % signal_name,
                )

            signal.send(sender=None, full_json=full_json)
