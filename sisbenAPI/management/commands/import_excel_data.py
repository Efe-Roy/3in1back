import os
import pandas as pd
from django.core.management.base import BaseCommand
from sisbenAPI.models import SisbenMain

class Command(BaseCommand):
    help = 'Import data from CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='CSV file name located in the same directory as manage.py')

    def handle(self, *args, **options):
        file_path = options['file_path']
        data = pd.read_excel(file_path)

        objects = [SisbenMain(**row) for _, row in data.iterrows()]

        SisbenMain.objects.bulk_create(objects)

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
