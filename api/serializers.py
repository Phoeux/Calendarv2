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

    class Meta:
        model = Holiday
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
    
    def to_internal_value(self, data):
        value = super(EventSerializer, self).to_internal_value(data)
        value['event_time'] = value['date'] - value['reminder']
        return value
