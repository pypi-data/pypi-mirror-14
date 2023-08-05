from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Download the assets into local folder'

    def add_arguments(self, parser):
        parser.add_argument('assets name', nargs='+', type=str)

    def handle(self, *args, **options):
        pass
