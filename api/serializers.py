from datetime import timedelta

from django.db.models import F, DateTimeField, ExpressionWrapper
from rest_framework import serializers

from api.models import Users, Country, Event, Holiday


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class HolidaySerializer(serializers.ModelSerializer):
    # location = serializers.ChoiceField

    class Meta:
        model = Holiday
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    # REMINDER = [
    #         (None, '---'),
    #         (timedelta(hours=1), 'За час'),
    #         (timedelta(hours=2), 'За 2 часа'),
    #         (timedelta(hours=4), 'За 4 часа'),
    #         (timedelta(days=1), 'За 1 день'),
    #         (timedelta(weeks=1), 'За неделю')
    #     ]
    # reminder = serializers.ChoiceField(REMINDER, default=REMINDER[0])

    class Meta:
        model = Event
        fields = '__all__'
    
    def to_internal_value(self, data):
        value = super(EventSerializer, self).to_internal_value(data)
        value['event_time'] = value['date'] - value['reminder']
        # value['creator'] = Users.objects.get(id=value['creator'].id)
        # value.pop(value['reminder'])
        return value
        

class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'
