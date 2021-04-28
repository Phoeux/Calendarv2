from django.contrib import admin

from api.models import Users, Country, Event, Holiday

admin.site.register(Users)
admin.site.register(Country)
admin.site.register(Event)
admin.site.register(Holiday)
