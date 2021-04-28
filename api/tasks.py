import requests
from celery import shared_task
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.db.models.functions import Now
from ics import Calendar

from api.models import Country, Holiday, Event


@shared_task
def country_parsing():
    url = 'https://www.officeholidays.com/countries'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    data = soup.find_all("div", {'class': 'four omega columns'})
    countries = []
    for i in data:
        for x in i.find_all('a'):
            countries.append(x.text.strip())
    Country.objects.bulk_create([Country(title=val) for val in countries])


@shared_task
def holiday_parsing():
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


@shared_task()
def event_check(event_pk):
    event = Event.objects.select_related('creator').get(pk=event_pk)
    subject = f"Событие {event.title}"
    message = (f"Сегодня в {event.date.year}/{event.date.month}/{event.date.day} "
               f"{event.date.hour}:{event.date.minute}:{event.date.second} предстоит событие\n {event.text}")
    from_email = 'lobinsky.gleb@gmail.com'
    to_email = event.creator.email
    send_mail(subject, message, from_email, [to_email])
    event.sended_notification = True
    event.save()


@shared_task()
def clear_expired_events():
    Event.objects.filter(date__lte=Now()).delete()
