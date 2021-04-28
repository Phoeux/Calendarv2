import requests
from django.core.management import BaseCommand
from bs4 import BeautifulSoup

from api.models import Country


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = 'https://www.officeholidays.com/countries'
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        data = soup.find_all("div", {'class': 'four omega columns'})
        countries = []
        for i in data:
            for x in i.find_all('a'):
                countries.append(x.text.strip())
        Country.objects.bulk_create([Country(title=val) for val in countries])