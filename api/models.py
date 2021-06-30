from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta
from django.utils import timezone


class Users(AbstractUser):
    country = models.ForeignKey('Country', on_delete=models.CASCADE, null=True)


class Country(models.Model):
    title = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.title


class Holiday(models.Model):
    title = models.CharField(max_length=200)
    begin_date = models.DateTimeField(default=None)
    end_date = models.DateTimeField()
    description = models.TextField(default=None)
    location = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)


class Event(models.Model):
    REMINDER = [
        (None, '---'),
        (timedelta(hours=1), 'За час'),
        (timedelta(hours=2), 'За 2 часа'),
        (timedelta(hours=4), 'За 4 часа'),
        (timedelta(days=1), 'За 1 день'),
        (timedelta(weeks=1), 'За неделю')
    ]

    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    reminder = models.DurationField(choices=REMINDER, default=None, max_length=20)
    creator = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user_event')
    event_time = models.DateTimeField(default=timezone.now, blank=True)
    sended_notification = models.BooleanField(default=False)
