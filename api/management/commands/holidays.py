import requests
from django.core.management import BaseCommand
from ics import Calendar

from api.models import Country, Holiday


class Command(BaseCommand):
    def handle(self, *args, **options):
        Holiday.objects.all().delete()
        for country in Country.objects.all():
            url = f'https://www.officeholidays.com/ics/ics_country.php?tbl_country={country}'
            data = requests.get(url).text
            try:
                holiday = Calendar(data).events
                for data in holiday:
                    Holiday.objects.create(
                        title=data.name.split(': ')[1],
                        begin_date=data.begin.datetime,
                        end_date=data.end.datetime,
                        description=data.description,
                        location=Country.objects.get(title=data.location)
                    )
            except:
                pass
