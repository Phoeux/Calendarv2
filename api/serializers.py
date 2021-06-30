from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers

from api.models import Users, Country, Event, Holiday


class UserSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class HolidaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Holiday
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    event_time2=serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['title', 'date', 'reminder', 'creator', 'event_time2']
    
    def to_internal_value(self, data):
        value = super(EventSerializer, self).to_internal_value(data)
        value['event_time'] = value['date'] - value['reminder']
        return value

    def get_event_time2(self, data):
        event_time2 = data.date - data.reminder
        return event_time2
