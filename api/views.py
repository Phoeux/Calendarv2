from datetime import datetime, timedelta

from django.db.models import F, ExpressionWrapper, DateTimeField
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.models import Users, Country, Event, Holiday
from api.serializers import UserSerializer, CountrySerializer, EventSerializer, HolidaySerializer

from api.tasks import event_check


class UserModelViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class CountryModelViewset(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']
    permission_classes = [IsAuthenticatedOrReadOnly]


class EventModelViewset(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    # permission_classes = [IsAuthenticated]

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     # Event.objects.filter(title=request.data['title']).update(event_time=ExpressionWrapper(
    #     #     F('date') + F('reminder'), output_field=DateTimeField()))
    #     headers = self.get_success_headers(serializer.data)
    #
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        data = super(EventModelViewset, self).perform_create(serializer)
        # data = serializer.save()
        # print(data.event_time)
        # time = datetime.utcnow() + timedelta(minutes=2)
        # print(time)
        # event_check.apply_async(args=[data.pk], eta=data.event_time)
        event_check.apply_async(args=[serializer.instance.pk], eta=serializer.instance.event_time)
        return data


class HolidayModelViewset(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        country = self.request.user.country
        queryset = Holiday.objects.filter(location=country)
        return queryset
